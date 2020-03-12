from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import address
from random import randint
from travel_planner_app.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("en_US")
        cities = City.objects.all()
        for city in cities:
            for _ in range(2):
                Airport.objects.create(
                    name=fake.street_name(),
                    IATA_code=fake.lexify(text='????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                    city=city
                )
        self.stdout.write("Dodano lotniska do miast")