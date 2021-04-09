import logging

import dgeq
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.core.serializers.json import DjangoJSONEncoder

from pl_sandbox.models import Sandbox


logger = logging.getLogger(__name__)



@shared_task
def poll_usage(sandbox_pk: int) -> None:
    """Poll usage of a sandbox and send it to the correct group."""
    sandbox = Sandbox.objects.get(pk=sandbox_pk)
    usage = async_to_sync(sandbox.poll_usage)()
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        f"sandbox_usage_{sandbox_pk}",
        {
            'type':  'sandbox_usage',
            'usage': DjangoJSONEncoder().encode(dgeq.serialize(usage))
        }
    )



@shared_task
def poll_specifications(sandbox_pk: int) -> None:
    """Poll specifications of a sandbox and send it to the correct group."""
    sandbox = Sandbox.objects.get(pk=sandbox_pk)
    sandbox_specs, container_specs = async_to_sync(sandbox.poll_specifications)()
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        f"sandbox_sandbox_specs_{sandbox_pk}",
        {
            'type':  'sandbox_specs',
            'specs': DjangoJSONEncoder().encode(dgeq.serialize(sandbox_specs))
        }
    )
    async_to_sync(channel_layer.group_send)(
        f"sandbox_container_specs_{sandbox_pk}",
        {
            'type':  'container_specs',
            'specs': DjangoJSONEncoder().encode(dgeq.serialize(container_specs))
        }
    )
