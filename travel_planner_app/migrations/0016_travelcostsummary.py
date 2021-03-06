# Generated by Django 3.0.4 on 2020-05-13 17:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_planner_app', '0015_delete_travelcostsummary'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelCostSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.IntegerField(null=True)),
                ('employee_name', models.CharField(max_length=128, null=True)),
                ('travel_date', models.DateField(null=True)),
                ('visa_cost', models.DecimalField(decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('hotel_cost', models.DecimalField(decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('total_travel_cost', models.DecimalField(decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
            options={
                'db_table': 'v_travel_cost_summary',
                'managed': False,
            },
        ),
    ]
