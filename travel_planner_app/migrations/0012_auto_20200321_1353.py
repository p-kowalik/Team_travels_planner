# Generated by Django 3.0.4 on 2020-03-21 13:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_planner_app', '0011_auto_20200313_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='cost_per_night',
            field=models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
