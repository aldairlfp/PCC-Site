# Generated by Django 4.0.6 on 2022-07-16 23:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_militant_is_removed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='militant',
            name='age',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='birth_year',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='cell_phone',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='fundator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='militant',
            name='house_phone',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='institutional_reserve_positon',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='job',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='job_clasification',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='no_ci',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='observations',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='pcc_position',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='pcc_reserve_position',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='scolarity',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='skin_color',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='work_file',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='militant',
            name='work_phone',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='militant',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 17, 0, 40, 53, 165595)),
        ),
    ]
