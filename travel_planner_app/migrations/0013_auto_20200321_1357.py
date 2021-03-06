# Generated by Django 3.0.4 on 2020-03-21 13:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_planner_app', '0012_auto_20200321_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_cost',
            field=models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='visa',
            name='visa_cost',
            field=models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
