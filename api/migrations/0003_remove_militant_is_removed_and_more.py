# Generated by Django 4.0.4 on 2022-06-16 22:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_militant_register_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='militant',
            name='is_removed',
        ),
        migrations.AlterField(
            model_name='militant',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 22, 3, 26, 463107)),
        ),
    ]
