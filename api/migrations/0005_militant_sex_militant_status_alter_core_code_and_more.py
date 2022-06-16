# Generated by Django 4.0.4 on 2022-06-15 23:30

import api.models
import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_core_code_alter_core_district_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='militant',
            name='sex',
            field=models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], default='Masculino', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='militant',
            name='status',
            field=models.CharField(choices=[('Casado/a', 'Casado/A'), ('Soltero/a', 'Soltero/A'), ('Divorciado/a', 'Divorciado/A')], default='Soltero', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='core',
            name='code',
            field=models.CharField(max_length=5, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(5, message='Min length of code must have more than 4 numbers.'), django.core.validators.MaxLengthValidator(5, message='Min length of code must have less than 6 numbers.'), api.models.validate_int_number]),
        ),
        migrations.AlterField(
            model_name='core',
            name='district',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='District cannot be empty.')]),
        ),
        migrations.AlterField(
            model_name='core',
            name='municipality',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1, message='Municipality cannot be empty.')]),
        ),
        migrations.AlterField(
            model_name='core',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1, message='Name cannot be empty.')]),
        ),
        migrations.AlterField(
            model_name='core',
            name='political_area',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1, message='Political area cannot be empty.')]),
        ),
        migrations.AlterField(
            model_name='core',
            name='province',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1, message='Province cannot be empty.')]),
        ),
        migrations.AlterField(
            model_name='core',
            name='sector',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1, message='Sector cannot be empty.')]),
        ),
        migrations.AlterField(
            model_name='core',
            name='subordinate',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1, message='Subordinate cannot be empty.')]),
        ),
        migrations.AlterField(
            model_name='militant',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 15, 23, 30, 14, 369685)),
        ),
    ]