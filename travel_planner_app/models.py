from django.contrib.auth.models import User
from django.db import models
from django.core.validators import EmailValidator, URLValidator, MinValueValidator


class Country(models.Model):
    name = models.CharField(max_length=64)
    time_to_obtain_visa = models.IntegerField(null=True)
    advance_days_required = models.IntegerField(default=7)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.country) + str(" ") + str(self.name)


class Airport(models.Model):
    name = models.CharField(max_length=64)
    IATA_code = models.CharField(max_length=6)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.city) + str("; IATA code: ") + str(self.IATA_code) + str("; airport name") + str(self.name)


class Ticket(models.Model):
    travel_booking_summary = models.ForeignKey('TravelBookingSummary', on_delete=models.CASCADE)
    travel_date_start = models.DateField()
    travel_date_end = models.DateField()
    airport_departure = models.CharField(max_length=128)
    airport_arrival = models.CharField(max_length=128)
    ticket_cost = models.DecimalField(max_digits=7, decimal_places=2,  validators=[MinValueValidator(0.00)])
    supervisor_approval = models.BooleanField(default=False)


class Visa(models.Model):
    travel_booking_summary = models.ForeignKey('TravelBookingSummary', on_delete=models.CASCADE)
    issued_on = models.DateField()
    validity_days = models.IntegerField()
    extension_option = models.NullBooleanField(default=False)
    visa_cost = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.00)])


class Hotel(models.Model):
    name = models.CharField(max_length=64)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone = models.CharField(max_length=30, null=True)
    email = models.EmailField(null=True)
    cost_per_night = models.DecimalField(max_digits=7, decimal_places=2,  validators=[MinValueValidator(0.00)])

    def __str__(self):
        return str(self.city) + str("; Hotel: ") + str(self.name)


class HotelBooking(models.Model):
    travel_booking_summary = models.ForeignKey('TravelBookingSummary', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()


class TravelBookingSummary(models.Model):
    travel_calendar = models.ForeignKey('TravelCalendar', on_delete=models.CASCADE)
    employee_comment = models.TextField(null=True)
    supervisor_comment = models.TextField(null=True)

    def __str__(self):
        return str(self.travel_calendar)


class TravelCalendar(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    travel_date_start = models.DateField()
    travel_date_end = models.DateField()
    city_from = models.ForeignKey('City', on_delete=models.CASCADE)
    city_destination = models.CharField(max_length=64)
    country_destination = models.CharField(max_length=64)
    travel_purpose_description = models.TextField(null=True)
    employee_approval = models.NullBooleanField(default=True)
    supervisor_approval = models.NullBooleanField(default=False)
    notification_advance = models.IntegerField(default=14)

    def __str__(self):
        return str(self.id) + str(self.employee) + str("; travel start: ") + str(self.travel_date_start)\
               + str("; travel end: ") + str(self.travel_date_end)


# class Employee(AbstractUser):
class Employee(models.Model):
    forename = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    passport_no = models.CharField(max_length=128)
    passport_validity = models.DateField()
    birthday = models.DateField()
    nationality = models.CharField(max_length=128)
    residence_country = models.CharField(max_length=128)
    residence_city = models.CharField(max_length=128)
    address = models.TextField()
    phone = models.CharField(max_length=128)
    email = models.EmailField()
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    # invitiation_code = models.CharField(max_length=140)

    def __str__(self):
        return str(self.surname) + str(" ") + str(self.forename)
