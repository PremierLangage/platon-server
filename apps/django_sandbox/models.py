import asyncio
import json
import logging
import traceback
from typing import Any, BinaryIO, Dict, Optional, Tuple, Union

from aiohttp import ClientError
from channels.db import database_sync_to_async
from dateutil.parser import isoparse
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import URLValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from sandbox_api import ASandbox

from django_sandbox.exceptions import SandboxDisabledError


logger = logging.getLogger(__name__)



class Sandbox(models.Model):
    """Represents a Sandbox server."""
    name = models.CharField(max_length=256, unique=True)
    url = models.CharField(
        max_length=2048, validators=[URLValidator(schemes=['http', 'https'])], unique=True
    )
    enabled = models.BooleanField()
    
    
    class Meta:
        verbose_name_plural = "Sandboxes"
    
    
    def __str__(self):
        return f"<Sandbox - {self.name} ({self.pk})>"
    
    
    @receiver(post_save, sender='django_sandbox.Sandbox')
    def create_periodic_tasks(sender, instance, created, **kwargs):
        """Create a periodic tasks to poll specs and usage of this Sandbox."""
        if created:
            usage_schedule, created = IntervalSchedule.objects.get_or_create(
                every=settings.SANDBOX_POLL_USAGE_EVERY, period=IntervalSchedule.SECONDS
            )
            specs_schedule, created = IntervalSchedule.objects.get_or_create(
                every=settings.SANDBOX_POLL_SPECS_EVERY,
                period=IntervalSchedule.SECONDS
            )
            logger.info(f"Creating periodic task to poll usage of sandbox {instance}")
            PeriodicTask.objects.create(
                name=f"sandbox_poll_usage_{instance.pk}", interval=usage_schedule,
                task='django_sandbox.tasks.poll_usage', args=json.dumps([instance.pk])
            )
            logger.info(f"Creating periodic task to poll specifications of sandbox {instance}")
            PeriodicTask.objects.create(
                name=f"sandbox_poll_specifications_{instance.pk}", interval=specs_schedule,
                task='django_sandbox.tasks.poll_specifications', args=json.dumps([instance.pk])
            )
    
    
    async def poll_specifications(self) -> Tuple['SandboxSpecs', 'ContainerSpecs']:
        """Poll the specifications of the sandbox's host and its containers.
        
        The sandbox must be enabled, `SandboxDisabledError` will be raised
        otherwise."""
        if not self.enabled:
            raise SandboxDisabledError("Cannot poll specifications of a disabled sandbox")
        
        async with ASandbox(self.url) as asandbox:
            raw_specs, libs = await asyncio.gather(asandbox.specifications(), asandbox.libraries())
        
        host, container = raw_specs["host"], raw_specs["container"]
        
        aw1 = database_sync_to_async(SandboxSpecs.objects.filter(sandbox=self).update)(
            polled=True, sandbox_version=host["sandbox_version"],
            docker_version=host["docker_version"], cpu_core=host["cpu"]["core"],
            cpu_logical=host["cpu"]["logical"], cpu_freq_min=host["cpu"]["freq_min"],
            cpu_freq_max=host["cpu"]["freq_max"], memory_ram=host["memory"]["ram"],
            memory_swap=host["memory"]["swap"], memory_storage=host["memory"]["storage"]
        )
        aw2 = database_sync_to_async(ContainerSpecs.objects.filter(sandbox=self).update)(
            polled=True, working_dir_device=container["working_dir_device"],
            count=container["count"], process=container["process"],
            cpu_count=container["cpu"]["count"], cpu_period=container["cpu"]["period"],
            cpu_shares=container["cpu"]["shares"], cpu_quota=container["cpu"]["quota"],
            memory_ram=container["memory"]["ram"], memory_swap=container["memory"]["swap"],
            memory_storage=container["memory"]["storage"],
            writing_io=container["io"]["read_iops"], writing_bytes=container["io"]["read_bps"],
            reading_io=container["io"]["write_iops"], reading_bytes=container["io"]["write_bps"],
            libraries=libs["libraries"], bin=libs["bin"]
        )
        await asyncio.gather(aw1, aw2)
        
        host = await database_sync_to_async(SandboxSpecs.objects.get)(sandbox=self)
        container = await database_sync_to_async(ContainerSpecs.objects.get)(sandbox=self)
        
        return host, container
    
    
    async def poll_usage(self) -> 'Usage':
        """Poll the current usage of the Sandbox.
        
        If the sandbox is disabled, a `SandboxUsage` with its field `enabled`
        will be produced, all the other fields, with the exception of `sandbox`
        and `date` will be None."""
        if not self.enabled:
            return await database_sync_to_async(Usage.objects.create)(
                sandbox=self, enabled=False
            )
        
        try:
            async with ASandbox(self.url) as asandbox:
                raw = await asandbox.usage()
            
            usage = await database_sync_to_async(Usage.objects.create)(
                sandbox=self, cpu_usage=[raw["cpu"]["usage"]] + raw["cpu"]["usage_avg"],
                cpu_freq=raw["cpu"]["frequency"], memory_ram=raw["memory"]["ram"],
                memory_swap=raw["memory"]["swap"], memory_storage=raw["memory"]["storage"],
                writing_io=raw["io"]["read_iops"], writing_bytes=raw["io"]["read_bps"],
                reading_io=raw["io"]["write_iops"], reading_bytes=raw["io"]["write_bps"],
                process=raw["process"], container=raw["container"],
                sending_packets=raw["network"]["sent_packets"],
                sending_bytes=raw["network"]["sent_bytes"],
                receiving_packets=raw["network"]["received_packets"],
                receiving_bytes=raw["network"]["received_bytes"]
            )
        except ClientError:
            usage = await database_sync_to_async(Usage.objects.create)(
                sandbox=self, reached=False
            )
        
        return usage
    
    
    async def execute(self, user: Union[AnonymousUser, User], config: Dict[str, Any],
                      environment: BinaryIO = None) -> 'Request':
        """Execute a request on the Sandbox based on `config` and
        `environment`.
        
        `environment` can be an optional binary stream representing the tgz
        containing the environment.
        
        `config` must be a dictionary containing information about the
         execution :
         
         * Mandatory key :
            * `commands` - A list of bash command to be executed. A failing
               command (exit code different than 0) will stop the sandbox,
               except if the command start with an hyphen -. Each command
               can also specify a timeout in seconds, like in the example.
         * Optional keys :
            * `result_path` - Path to the file from which the result field
               of the response will be extracted. if result_path is absent
               from the request, result will not be present in the response.
            * `environ` - A list of environments variables as dictionary
               containing the var name and its value.
            * `environment` - Use this environment stored in the sandbox as
               a base environment. File present in this function's
               environment will be added to this environment (file with the
               same name are overwritten).
            * `save` - Boolean indicating if the resulting environment
               should be saved. If true, the environment's UUID will be sent
               in the response in the field environment. It'll be kept on
               the sandbox for a time define in the sandbox's settings.
               That expiration date will be sent in the response in the
               `expire` field (ISO 8601 format). If the field save is
               missing, it is assumed to be False.
               
        The sandbox must be enabled, a failed SandboxExecution will be produced
        otherwise."""
        try:
            if not self.enabled:
                raise SandboxDisabledError("Cannot execute on a disabled sandbox")
            
            async with ASandbox(self.url) as asandbox:
                r = await asandbox.execute(config, environment)
            
            response = await database_sync_to_async(Response.objects.create)(
                status=r["status"], total_time=r["total_time"], result=r.get("result", ""),
                environment=r.get("environment", ""),
                expire=isoparse(r["expire"]) if "expire" in r else None
            )
            
            for e in r["execution"]:
                await database_sync_to_async(CommandResult.objects.create)(
                    response=response, command=e["command"], exit_code=e["exit_code"],
                    stdout=e["stdout"], stderr=e["stderr"], time=e["time"]
                )
            
            execution = await database_sync_to_async(Request.objects.create)(
                sandbox=self, config=config, success=True, response=response,
                user=user if user.is_authenticated else None
            )
        
        except ClientError as e:
            execution = await database_sync_to_async(Request.objects.create)(
                sandbox=self, config=config, success=False, traceback=traceback.format_exc(),
                response=None, user=user if user.is_authenticated else None
            )
            logger.warning(
                f"Execution failed on sandbox {self}, see execution of id '{execution.pk}'",
                exc_info=e
            )
        
        except SandboxDisabledError:
            execution = await database_sync_to_async(Request.objects.create)(
                sandbox=self, config=config, success=False, traceback=traceback.format_exc(),
                response=None, user=user if user.is_authenticated else None
            )
            logger.warning(f"Execution failed on sandbox {self} because it was disabled,"
                           f"see execution of id '{execution.pk}'")
        
        return execution
    
    
    async def retrieve(self, environment: str, file: str = None) -> Optional[BinaryIO]:
        """Download an environment of the Sandbox.
        
        The sandbox must be enabled, `SandboxDisabledError` will be raised
        otherwise.
        
        If `file` is given, it must be the path of a file inside the
        environment, only this file will be downloaded."""
        if not self.enabled:
            raise SandboxDisabledError("Cannot execute on a disabled sandbox")
        
        async with ASandbox(self.url) as asandbox:
            return await asandbox.download(environment, file)



class SandboxSpecs(models.Model):
    """Contains the specifications of the computer hosting the Sandbox.
    
    Fields :
    
    * `sandbox` (`Sandbox`) - Sandbox these specifications corresponds to.
    * `polled` (`bool`) - Whether the specifications has been polled.
    * `sandbox_version` (`str`) - Version of the Sandbox.
    * `docker_version` (`str`) - Version of Docker used by the Sandbox.
    * `cpu_core` (`int`) - Number of physical core.
    * `cpu_logical` (`int`) - Number of logical core.
    * `cpu_freq_min` (`float`) - Minimum frequency of the CPU (in MHz)
    * `cpu_freq_max` (`float`) - Maximum frequency of the CPU (in MHz)
    * `memory_ram` (`int`) - Total RAM available on the host (in bytes).
    * `memory_swap` (`int`) - Total swap available on the host (in bytes).
    * `memory_storage` (`dict`) - Dictionary mapping host's mounted
       filesystems to their size (in bytes).
    
    Every field but `sandbox` and `polled` will be None as long as `polled` is
    False."""
    sandbox = models.OneToOneField(
        Sandbox, related_name="server_specs", on_delete=models.CASCADE
    )
    polled = models.BooleanField(default=False)
    sandbox_version = models.CharField(max_length=64, null=True, blank=True, default=None)
    docker_version = models.CharField(max_length=64, null=True, blank=True, default=None)
    cpu_core = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    cpu_logical = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    cpu_freq_min = models.FloatField(null=True, blank=True, default=None)
    cpu_freq_max = models.FloatField(null=True, blank=True, default=None)
    memory_ram = models.BigIntegerField(null=True, blank=True, default=None)
    memory_swap = models.BigIntegerField(null=True, blank=True, default=None)
    memory_storage = models.JSONField(null=True, blank=True, default=None)
    
    
    class Meta:
        verbose_name = "Sandbox Specifications"
        verbose_name_plural = "Sandbox Specifications"
    
    
    @receiver(post_save, sender=Sandbox)
    def create(sender, instance, created, **kwargs):
        """When a new Sandbox is created, create the corresponding
        SandboxSpecs."""
        if created:
            SandboxSpecs.objects.create(sandbox=instance)



class ContainerSpecs(models.Model):
    """Contains the specifications used by the container on the Sandbox.
    
    Contains the specifications of the computer hosting the Sandbox.

    Fields :
    
    * `sandbox` (`Sandbox`) - Sandbox these specifications corresponds to.
    * `polled` (`bool`) - Whether the specifications has been polled.
    * `working_dir_device` (`str`) - Filesystem containers are running on.
    * `count` (`int`) - Total number of container available on the Sandbox.
    * `process` (`int`) - Limit of process running in a container.
    * `cpu_count` (`int`) - Number of logical core available to the sandbox.
    * `cpu_period` (`int`) - CPU CFS (Completely Fair Scheduler) period
       limit in a container (see link below).
    * `cpu_shares` (`int`) - CPU shares in a container (relative weight, see
       link below).
    * `cpu_quota` (`int`) - CPU CFS quota in a running container (see link
        below)
    * `memory_ram` (`int`) - The maximum amount of RAM a container can use
       (in bytes).
    * `memory_swap` (`int`) -  The maximum amount of swap a container can
       use (in bytes).
    * `memory_storage` (`int`) - The maximum amount of storage a container
       can use on `working_dir_device` (in bytes).
    * `writing_io` (`dict`) - Dictionary mapping mounted filesystems to
       their limit write rate (IO per second).
    * `writing_bytes (`dict`) - Dictionary mapping mounted filesystems to
       their limit write rate (bytes per second).
    * `reading_io` (`dict`) - Dictionary mapping mounted filesystems to
       their limit read rate (IO per second).
    * `reading_bytes` (`dict`) - Dictionary mapping mounted filesystems to
       their limit read rate (bytes per second).
    * `bin` (`list`) - List of available bash command inside a container.
    * `libraries` ('dict`) - Dictionary listing libraries installed for the
       system and the main programming language in the form:
       ```
       libraries": {
           "system": {
               "[lib]": "[version]"
               [...]
           },
           "[language1]": {
               [...]
          }
           [...]
       }
       ```
       
    A value of -1 in a field means that there is no limit.
    
    Every field but `sandbox` and `polled` will be None as long as `polled` is
    False.
    
    cpu period:
    https://docs.docker.com/engine/reference/run/#cpu-period-constraint
    cpu share :
    https://docs.docker.com/engine/reference/run/#cpu-share-constraint
    cpu share :
    https://docs.docker.com/engine/reference/run/#cpu-quota-constraint"""
    sandbox = models.OneToOneField(
        Sandbox, related_name="container_specs", on_delete=models.CASCADE
    )
    polled = models.BooleanField(default=False)
    working_dir_device = models.CharField(max_length=128, null=True, blank=True, default=None)
    count = models.SmallIntegerField(null=True, blank=True, default=None)
    process = models.SmallIntegerField(null=True, blank=True, default=None)
    cpu_count = models.SmallIntegerField(null=True, blank=True, default=None)
    cpu_period = models.SmallIntegerField(null=True, blank=True, default=None)
    cpu_shares = models.SmallIntegerField(null=True, blank=True, default=None)
    cpu_quota = models.SmallIntegerField(null=True, blank=True, default=None)
    memory_ram = models.BigIntegerField(null=True, blank=True, default=None)
    memory_swap = models.BigIntegerField(null=True, blank=True, default=None)
    memory_storage = models.BigIntegerField(null=True, blank=True, default=None)
    writing_io = models.JSONField(null=True, blank=True, default=None)
    writing_bytes = models.JSONField(null=True, blank=True, default=None)
    reading_io = models.JSONField(null=True, blank=True, default=None)
    reading_bytes = models.JSONField(null=True, blank=True, default=None)
    libraries = models.JSONField(null=True, blank=True, default=None)
    bin = ArrayField(models.CharField(max_length=64), null=True, blank=True, default=None)
    
    
    class Meta:
        verbose_name = "Container Specifications"
        verbose_name_plural = "Container Specifications"
    
    
    @receiver(post_save, sender=Sandbox)
    def create(sender, instance, created, **kwargs):
        """When a new Sandbox is created, create the corresponding
        ContainerSpecs."""
        if created:
            ContainerSpecs.objects.create(sandbox=instance)



class Usage(models.Model):
    """Represents the usage of a Sandbox at the given datetime.
    
    Fields :
    
    * `sandbox` (`Sandbox`) - Sandbox this `SandboxUsage` corresponds to.
    * `date` (`datetime`) - Date this `SandboxUsage` was polled.
    * `enabled` (`bool`) - Whether the sandbox was enabled.
    * `reached` (`bool`) - Whether the polling request succeeded.
    * `cpu_usage` (`list`) - List of 4 `float` containing the average cpu
       usage rate now, and in the last 1 minutes, 5 minutes and 15 minutes.
       0 means no usage, 1 means every core a running at 100%.
    * `cpu_freq` (`float`) - Current frequency of the CPU in MHz.
    * `memory_ram` (`int`) - Current RAM used on the host (in bytes).
    * `memory_swap` (`int`) - Total swap used on the host (in bytes).
    * `memory_storage` (`dict`) - Dictionary mapping host's mounted
       filesystems to their usage (in bytes).
    * `writing_io` (`dict`) - Dictionary mapping mounted filesystems to
       current write rate (IO per second).
    * `writing_bytes (`dict`) - Dictionary mapping mounted filesystems to
       their current write rate (bytes per second).
    * `reading_io` (`dict`) - Dictionary mapping mounted filesystems to
       their current read rate (IO per second).
    * `reading_bytes` (`dict`) - Dictionary mapping mounted filesystems to
       their current read rate (bytes per second).
    * `sending_packets` (`int`) - Network sent data rate (in packets per
       second)
    * `sending_bytes` (`int`) - Network sent data rate (in bytes per
       second)
    * `receiving_packets` (`int`) - Network received data rate (in packets
       per second)
    * `receiving_bytes` (`int`) - Network received data rate (in bytes per
       second)
    * `process` (`int`) - Number of process currently running.
    * `container` (`int`) - Number of container currently used.
    
    If `enabled` or `reached` are False, every other fields but `sandbox` and
    `date` are None.
    
    Disk and network I/O are the average of the last 2 seconds."""
    sandbox = models.ForeignKey(Sandbox, related_name="usages", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)
    reached = models.BooleanField(default=True)
    cpu_usage = ArrayField(models.FloatField(), null=True, blank=True, size=4)
    cpu_freq = models.FloatField(null=True, blank=True)
    memory_ram = models.BigIntegerField(null=True, blank=True)
    memory_swap = models.BigIntegerField(null=True, blank=True)
    memory_storage = models.JSONField(null=True, blank=True)
    writing_io = models.JSONField(null=True, blank=True)
    writing_bytes = models.JSONField(null=True, blank=True)
    reading_io = models.JSONField(null=True, blank=True)
    reading_bytes = models.JSONField(null=True, blank=True)
    sending_packets = models.BigIntegerField(null=True, blank=True)
    sending_bytes = models.BigIntegerField(null=True, blank=True)
    receiving_packets = models.BigIntegerField(null=True, blank=True)
    receiving_bytes = models.BigIntegerField(null=True, blank=True)
    process = models.PositiveSmallIntegerField(null=True, blank=True)
    container = models.PositiveSmallIntegerField(null=True, blank=True)
    
    
    class Meta:
        ordering = ['-date', 'sandbox']
        indexes = [models.Index(fields=['-date'])]
        get_latest_by = "date"



class Response(models.Model):
    """Represents the response of a `SandboxExecution`
    
    Fields :
    
    * `status` (`int`) indicate whether the execution succeeded or failed :
        * `0` - The execution was successful, or the last command's failure was
            ignored (through the used of `-`).
        * `> 0` - The last command exited failed, `status` will be set to this
            command's exit code.
        * `< 0` - An error occurred on the sandbox.
    * `total_time` (`float`) - The total time taken by the whole execution
        request, it thus can be higher than the sum of each command's time.
    * `result` (`str`) - Set only if the `config` of the request contained
        `result_path`, correspond to the content of the file pointed by
        `result_path`.
    * `environment` (`str`) - Set only if `config` asked to save the
        environment. Contains the UUID of the environment on the sandbox
        server.
    * `expire` (`datetime`) - Set only if `config` asked to save the
        environment. Contains the date by which the environment will be deleted
        from the sandbox server.
    """
    status = models.IntegerField()
    total_time = models.FloatField()
    result = models.TextField(default="")
    environment = models.CharField(max_length=36, default="")
    expire = models.DateTimeField(null=True, blank=True)



class CommandResult(models.Model):
    """Represents the result of a single command in a `SandboxResponse`.
    
    Fields :
    
    * `response` (`SandboxResponse`) - Response this command is a part of.
    * `command` (`str`) - The command executed.
    * `exit_code` (`int`) - Exit code of the command.
    * `stdout` (`str`) - Everything written on *stdout* by the command.
    * `stderr` (`str`) - Everything written on *stderr* by the command.
    * `time` (`float`) - Execution's time taken by the command in second.
    """
    response = models.ForeignKey(Response, related_name="execution", on_delete=models.CASCADE)
    command = models.TextField()
    exit_code = models.IntegerField()
    stdout = models.TextField(default="")
    stderr = models.TextField(default="")
    time = models.FloatField()



class Request(models.Model):
    """Represents an execution on a Sandbox.
    
    Fields :
    
    * `sandbox` (`sandbox`) - Sandbox the execution took place on.
    * `user` (`User`) - User who requested the execution.
    * `date` (`datetime`) - Date of the execution.
    * `success` (`bool`) - Whether the sandbox accepted the request and
       responded correctly (does not mean that the execution succeeded).
    * `traceback` (`str`) - Traceback if the request failed.
    * `config` (`dict`) - Config dictionary use for this request.
    * `response` (`dictionary`) - Dictionary containing the response.
    
    `traceback` will be an empty string if `success` is True, and `response`
    will be None if `success` is False.
    """
    sandbox = models.ForeignKey(
        Sandbox, related_name="executions", null=True, on_delete=models.SET_NULL
    )
    response = models.OneToOneField(
        Response, related_name="request", null=True, on_delete=models.RESTRICT
    )
    user = models.ForeignKey(User, related_name="executions", null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    traceback = models.TextField(default="")
    config = models.JSONField()
    
    
    class Meta:
        ordering = ['-date', 'sandbox']
        indexes = [models.Index(fields=['-date'])]
        get_latest_by = "date"
