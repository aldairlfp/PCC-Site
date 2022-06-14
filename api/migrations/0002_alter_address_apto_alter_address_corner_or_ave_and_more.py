# Generated by Django 4.0.4 on 2022-06-14 04:02

import api.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='apto',
            field=models.CharField(max_length=100, validators=[api.models.validate_null_strings], verbose_name='No. Y/O APTO'),
        ),
        migrations.AlterField(
            model_name='address',
            name='corner_or_ave',
            field=models.CharField(max_length=100, validators=[api.models.validate_null_strings]),
        ),
        migrations.AlterField(
            model_name='address',
            name='municipality',
            field=models.CharField(max_length=100, validators=[api.models.validate_null_strings]),
        ),
        migrations.AlterField(
            model_name='address',
            name='neighborhood',
            field=models.CharField(max_length=100, validators=[api.models.validate_null_strings]),
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.CharField(max_length=100, validators=[api.models.validate_null_strings]),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=100, validators=[api.models.validate_null_strings]),
        ),
        migrations.AlterField(
            model_name='militant',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 14, 4, 2, 20, 86669)),
        ),
    ]