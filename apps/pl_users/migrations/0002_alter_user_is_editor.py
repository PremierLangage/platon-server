# Generated by Django 3.2.3 on 2021-05-25 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pl_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_editor',
            field=models.BooleanField(default=False, verbose_name='Editor'),
        ),
    ]
