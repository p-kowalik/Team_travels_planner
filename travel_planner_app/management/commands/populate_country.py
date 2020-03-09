from faker import Faker
from faker.providers import address
from random import randint
from django.core.management.base import BaseCommand
from travel_planner_app.models import Country


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("pl_PL")
        for _ in range(50):
            Country.objects.create(
                name=fake.country(),
                time_to_obtain_visa=randint(7, 15),
                advance_days_required=7
            )
        self.stdout.write("Dodano kraje")

