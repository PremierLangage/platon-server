# Generated by Django 3.2.5 on 2021-08-03 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pl_resources', '0008_remove_circle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('MEMBER', 'Member')], max_length=20),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.CharField(choices=[('MEMBER', 'Member')], max_length=20),
        ),
    ]
