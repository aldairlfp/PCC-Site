# Generated by Django 4.0.4 on 2022-06-16 03:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_payment_norm_paymentdeclaration_norm_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='militant',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 3, 57, 4, 641986)),
        ),
        migrations.AlterField(
            model_name='paymentdate',
            name='date',
            field=models.DateTimeField(primary_key=True, serialize=False),
        ),
    ]