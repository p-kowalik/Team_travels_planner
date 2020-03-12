from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import address
from random import randint
from travel_planner_app.models import *
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
            for _ in range(1):
                Hotel.objects.create(
                    name=fake.last_name(),
                    city=city,
                    address=fake.address(),
                    phone=fake.phone_number(),
                    email=fake.email(),
                    cost_per_night=fake.random_int(min=50, max=300, step=10)
                )
        self.stdout.write("Dodano hotel do miasta")