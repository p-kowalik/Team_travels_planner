from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import address
from random import randint
from travel_planner_app.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("en_US")
        for _ in range(200):
            Employee.objects.create(
                forename=fake.first_name(),
                surname=fake.last_name(),
                passport_no=fake.random_number(digits=None, fix_len=10),
                passport_validity=fake.date_between_dates(date_start='2020-01-01', date_end='2030-01-01'),
                birthday=fake.date_between_dates(date_start='1950-01-01', date_end='2000-01-01'),
                nationality=fake.country(),
                residence_country=fake.country(),
                residence_city=fake.city(),
                address=fake.address(),
                phone=fake.phone_number(),
                email=fake.email()
            )
        self.stdout.write("Dodano pracowników")