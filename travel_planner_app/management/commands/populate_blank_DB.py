from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from datetime import datetime
from faker import Faker
from faker.providers import address
from faker.providers import *  #sprawdzić które biblioteki są wymagane
from random import randint
from travel_planner_app.models import *


# step 1 - populate countries
class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("pl_PL")
        for _ in range(50):
            Country.objects.create(
                name=fake.country(),
                time_to_obtain_visa=randint(7, 15),
                advance_days_required=7
            )
        self.stdout.write("Countries added")

# step 2 - populate cities
        fake = Faker("")
        countries = Country.objects.all()
        for country in countries:
            for _ in range(10):
                City.objects.create(
                    name=fake.city(),
                    country=country
                )
        self.stdout.write("Cities added to countries")

# step 3 - populate hotels
        fake = Faker("en_US")
        cities = City.objects.all()
        for city in cities:
            for _ in range(1):
                Hotel.objects.create(
                    name=fake.last_name(),
                    city=city,
                    address=fake.address(),
                    phone=fake.phone_number(),
                    email=fake.email(),
                    cost_per_night=fake.random_int(min=50, max=300, step=10)
                )
        self.stdout.write("Hotels added to cities")

# step 4 - populate airports
        fake = Faker("en_US")
        cities = City.objects.all()
        for city in cities:
            for _ in range(2):
                Airport.objects.create(
                    name=fake.street_name(),
                    IATA_code=fake.lexify(text='????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                    city=city
                )
        self.stdout.write("Airports added to ctities")

# step 5 - populate employees
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
        self.stdout.write("Employees added")