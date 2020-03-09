from faker import Factory

from exercises.models import Student, SchoolSubject as Subject, SCHOOL_CLASS


def create_name():
    fake = Factory.create("pl_PL")
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name


def create_students():
    for school_class_key, _ in SCHOOL_CLASS:
        for kid in range(0, 20):
            first_name, last_name = create_name()
            Student.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   school_class=school_class_key)


def create_subjects():
    Subject.objects.create(name="Język polski", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Matematyka", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Język angielski", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Fizyka", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Wychowanie fizyczne", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Technika", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Biologia", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Chemia", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Geografia", teacher_name=" ".join(create_name()))



##################
from random import randint
from django.core.management.base import BaseCommand
from random import randrange
from faker import Faker
from faker.providers import date_time
from datetime import timedelta

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("pl_PL")
        for i in range(20):
            category = Categories()
            category.name = fake.text(max_nb_chars=20)
            category.description = fake.text(max_nb_chars=200)
            category.save()
            article = Article()
            article.title = fake.text(max_nb_chars=60)
            article.author = fake.name()
            article.content = fake.text(max_nb_chars=200)
            article.status = randint(1,3)
            article.date_of_emission_start = fake.date(pattern='%Y-%m-%d', end_datetime=None)  #fake.date_between_dates(date_start='1990-1-1', date_end='2000-1-1')
            article.date_of_emission_end = fake.date(pattern='%Y-%m-%d', end_datetime=None)  #fake.date_between_dates(date_start='1990-0-1', date_end='2000-1-1')
            article.save()


###################
from exercises.models import *
from random import randint
from django.core.management.base import BaseCommand
from random import randrange
from faker import Faker
from faker.providers import date_time
from datetime import timedelta

from random import randint
from django.core.management.base import BaseCommand
from exercises.models import Student, SchoolSubject, StudentGrades, GRADES
class Command(BaseCommand):
    def handle(self, *args, **options):
        students = Student.objects.all()
        subjects = SchoolSubject.objects.all()
        for student in students:
            for subject in subjects:
                for _ in range(10):
                    StudentGrades.objects.create(
                        student=student,
                        school_subject=subject,
                        grade=GRADES[randint(0, 15)][0]
                    )
        self.stdout.write("Dodano oceny dla wszystkich studentów i przedmiotów")



#############################
from django.core.management.base import BaseCommand
from ._private import create_students, create_subjects


class Command(BaseCommand):
    help = 'Populates school with students, subjects and teachers'

    def handle(self, *args, **options):
        create_students()
        self.stdout.write(self.style.SUCCESS("Succesfully populated school with students"))
        create_subjects()
        self.stdout.write(self.style.SUCCESS("Succesfully created subjects"))