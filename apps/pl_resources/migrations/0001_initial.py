# Generated by Django 3.2.7 on 2021-09-02 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.CharField(blank=True, default='Aucune description', max_length=300)),
                ('opened', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('desc', models.CharField(blank=True, default='', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('MODEL', 'Model'), ('ACTIVITY', 'Activity'), ('EXERCISE', 'Exercise')], max_length=20)),
                ('desc', models.CharField(blank=True, default='Aucune description', max_length=300)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('READY', 'Ready'), ('DEPRECATED', 'Deprecated'), ('BUGGED', 'Bugged'), ('NOT_TESTED', 'Not Tested')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to=settings.AUTH_USER_MODEL)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='pl_resources.circle')),
                ('levels', models.ManyToManyField(blank=True, related_name='resources', to='pl_resources.Level')),
                ('topics', models.ManyToManyField(blank=True, related_name='resources', to='pl_resources.Topic')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('MEMBER_CREATE', 'Member Create'), ('MEMBER_REMOVE', 'Member Remove'), ('RESOURCE_CREATE', 'Resource Create'), ('RESOURCE_STATUS_CHANGE', 'Resource Status Change')], max_length=50)),
                ('data', models.JSONField(blank=True, default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='pl_resources.circle')),
            ],
        ),
        migrations.AddField(
            model_name='circle',
            name='levels',
            field=models.ManyToManyField(blank=True, related_name='circles', to='pl_resources.Level'),
        ),
        migrations.AddField(
            model_name='circle',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pl_resources.circle'),
        ),
        migrations.AddField(
            model_name='circle',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='circles', to='pl_resources.Topic'),
        ),
        migrations.AddField(
            model_name='circle',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watched_circles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RecentView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pl_resources.resource')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
                'unique_together': {('user', 'item')},
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('MEMBER', 'Member')], max_length=20)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='pl_resources.circle')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'circle')},
            },
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('MEMBER', 'Member')], max_length=20)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='pl_resources.circle')),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='circle_invitations', to=settings.AUTH_USER_MODEL)),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('circle', 'invitee')},
            },
        ),
    ]
