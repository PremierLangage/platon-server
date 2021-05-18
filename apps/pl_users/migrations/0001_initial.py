# Generated by Django 3.1.6 on 2021-02-15 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import pl_lti.role


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', enumfields.fields.EnumIntegerField(default=0, enum=pl_lti.role.Role)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]