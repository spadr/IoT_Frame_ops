# Generated by Django 3.1.6 on 2021-07-27 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0003_auto_20210727_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devicemodel',
            old_name='latest',
            new_name='activity',
        ),
        migrations.RenameField(
            model_name='devicemodel',
            old_name='LD_min',
            new_name='interval',
        ),
        migrations.RenameField(
            model_name='devicemodel',
            old_name='LD_status',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='devicemodel',
            old_name='device_token',
            new_name='token',
        ),
    ]
