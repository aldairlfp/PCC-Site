# Generated by Django 4.0.4 on 2022-06-16 21:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='militant',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 21, 49, 14, 991710)),
        ),
    ]