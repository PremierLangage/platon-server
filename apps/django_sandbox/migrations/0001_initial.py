# Generated by Django 3.1.1 on 2020-09-23 14:52

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('total_time', models.FloatField()),
                ('result', models.TextField(default='')),
                ('environment', models.CharField(default='', max_length=36)),
                ('expire', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sandbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('url', models.CharField(max_length=2048, validators=[django.core.validators.URLValidator(schemes=['http', 'https'])])),
                ('enabled', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Sandboxes',
            },
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('enabled', models.BooleanField(default=True)),
                ('reached', models.BooleanField(default=True)),
                ('cpu_usage', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=4)),
                ('cpu_freq', models.FloatField(blank=True, null=True)),
                ('memory_ram', models.BigIntegerField(blank=True, null=True)),
                ('memory_swap', models.BigIntegerField(blank=True, null=True)),
                ('memory_storage', models.JSONField(blank=True, null=True)),
                ('writing_io', models.JSONField(blank=True, null=True)),
                ('writing_bytes', models.JSONField(blank=True, null=True)),
                ('reading_io', models.JSONField(blank=True, null=True)),
                ('reading_bytes', models.JSONField(blank=True, null=True)),
                ('sending_packets', models.BigIntegerField(blank=True, null=True)),
                ('sending_bytes', models.BigIntegerField(blank=True, null=True)),
                ('receiving_packets', models.BigIntegerField(blank=True, null=True)),
                ('receiving_bytes', models.BigIntegerField(blank=True, null=True)),
                ('process', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('container', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('sandbox', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usages', to='django_sandbox.sandbox')),
            ],
            options={
                'ordering': ['-date', 'sandbox'],
            },
        ),
        migrations.CreateModel(
            name='SandboxSpecs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polled', models.BooleanField(default=False)),
                ('sandbox_version', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('docker_version', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('cpu_core', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cpu_logical', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('cpu_freq_min', models.FloatField(blank=True, default=None, null=True)),
                ('cpu_freq_max', models.FloatField(blank=True, default=None, null=True)),
                ('memory_ram', models.BigIntegerField(blank=True, default=None, null=True)),
                ('memory_swap', models.BigIntegerField(blank=True, default=None, null=True)),
                ('memory_storage', models.JSONField(blank=True, default=None, null=True)),
                ('sandbox', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='server_specs', to='django_sandbox.sandbox')),
            ],
            options={
                'verbose_name': 'Sandbox Specifications',
                'verbose_name_plural': 'Sandbox Specifications',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField()),
                ('traceback', models.TextField(default='')),
                ('config', models.JSONField()),
                ('response', models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='request', to='django_sandbox.response')),
                ('sandbox', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='executions', to='django_sandbox.sandbox')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='executions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', 'sandbox'],
            },
        ),
        migrations.CreateModel(
            name='ContainerSpecs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polled', models.BooleanField(default=False)),
                ('working_dir_device', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('count', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('process', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('cpu_count', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('cpu_period', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('cpu_shares', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('cpu_quota', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('memory_ram', models.BigIntegerField(blank=True, default=None, null=True)),
                ('memory_swap', models.BigIntegerField(blank=True, default=None, null=True)),
                ('memory_storage', models.BigIntegerField(blank=True, default=None, null=True)),
                ('writing_io', models.JSONField(blank=True, default=None, null=True)),
                ('writing_bytes', models.JSONField(blank=True, default=None, null=True)),
                ('reading_io', models.JSONField(blank=True, default=None, null=True)),
                ('reading_bytes', models.JSONField(blank=True, default=None, null=True)),
                ('libraries', models.JSONField(blank=True, default=None, null=True)),
                ('bin', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), blank=True, default=None, null=True, size=None)),
                ('sandbox', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='container_specs', to='django_sandbox.sandbox')),
            ],
            options={
                'verbose_name': 'Container Specifications',
                'verbose_name_plural': 'Container Specifications',
            },
        ),
        migrations.CreateModel(
            name='CommandResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.TextField()),
                ('exit_code', models.IntegerField()),
                ('stdout', models.TextField(default='')),
                ('stderr', models.TextField(default='')),
                ('time', models.FloatField()),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='execution', to='django_sandbox.response')),
            ],
        ),
        migrations.AddIndex(
            model_name='usage',
            index=models.Index(fields=['-date'], name='django_sand_date_adf10a_idx'),
        ),
        migrations.AddIndex(
            model_name='request',
            index=models.Index(fields=['-date'], name='django_sand_date_586f48_idx'),
        ),
    ]
