# Generated by Django 3.1.6 on 2021-02-20 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pl_lti', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lms',
            options={'verbose_name_plural': 'LMS'},
        ),
        migrations.AlterModelOptions(
            name='lticourse',
            options={'verbose_name_plural': 'LTI courses'},
        ),
        migrations.AlterModelOptions(
            name='ltiuser',
            options={'verbose_name_plural': 'LTI users'},
        ),
        migrations.AlterField(
            model_name='lticourse',
            name='lms_course_id',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='ltiuser',
            name='lms_user_id',
            field=models.CharField(max_length=200),
        ),
    ]