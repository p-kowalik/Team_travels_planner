from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import address
from random import randint
from travel_planner_app.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("pl_PL")
        countries = Country.objects.all()
        for country in countries:
            for _ in range(10):
                City.objects.create(
                    name=fake.country(),
                    country=country
                )
        self.stdout.write("Dodano miasta do krajów")

