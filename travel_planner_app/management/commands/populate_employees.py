from django.core.management.base import BaseCommand
from datetime import datetime
from faker import Faker
from faker.providers import *  #sprawdzić które biblioteki są wymagane
from random import randint
from travel_planner_app.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("en_US")
        for _ in range(200):
            Employee.objects.create(
                forename=fake.first_name(),
                surname=fake.last_name(),
                passport_no=fake.random_int(min=1000000000, max=9999999999, step=1),
                passport_validity=fake.future_date(end_date='+10y', tzinfo=None),
                birthday=fake.date_of_birth(tzinfo=None, minimum_age=20, maximum_age=65),
                nationality=fake.country(),
                residence_country=fake.country(),
                residence_city=fake.city(),
                address=fake.address(),
                phone=fake.phone_number(),
                email=fake.email()
            )
        self.stdout.write("Dodano pracowników")