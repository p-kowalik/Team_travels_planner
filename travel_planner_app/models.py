from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=64)
    time_to_obtain_visa = models.IntegerField()
    advance_days_required = models.IntegerField(default=7)


class City(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)


class Airport(models.Model):
    name = models.CharField(max_length=64)
    IATA_code = models.CharField(max_length=5)
    city = models.ForeignKey('City', on_delete=models.CASCADE)


class Ticket(models.Model):
    travel_booking_summary = models.ForeignKey('TravelBookingSummary', on_delete=models.CASCADE)
    travel_date_start = models.DateField()
    travel_date_end = models.DateField()
    airport_departure = models.CharField(max_length=64)
    airport_arrival = models.CharField(max_length=64)
    ticket_cost = models.FloatField()
    supervisor_approval = models.BooleanField(default=False)


class Visa(models.Model):
    travel_booking_summary = models.ForeignKey('TravelBookingSummary', on_delete=models.CASCADE)
    issued_on = models.DateField()
    validity_days = models.IntegerField()
    extension_option = models.NullBooleanField
    visa_cost = models.FloatField()


class Hotel(models.Model):
    name = models.CharField(max_length=64)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=30)
    email = models.EmailField
    cost_per_night = models.FloatField()


class HotelBooking(models.Model):
    travel_booking_summary = models.ForeignKey('TravelBookingSummary', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    cost_per_stay = models.FloatField()


class TravelBookingSummary(models.Model):
    travel_calendar = models.ForeignKey('TravelCalendar', on_delete=models.CASCADE)
    employee_comment = models.TextField()
    supervisor_comment = models.TextField()


class TravelCalendar(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    travel_date_start = models.DateField()
    travel_date_end = models.DateField()
    country_from = models.DateField()
    country_destination = models.DateField()
    city_from = models.DateField()
    city_destination = models.DateField()
    travel_purpose_description = models.TextField()
    employee_approval = models.NullBooleanField
    supervisor_approval = models.NullBooleanField
    notification_advance = models.IntegerField(default=14)


class Employee(models.Model):
    forename = models.CharField(max_length=64)
    surename = models.CharField(max_length=64)
    passport_no = models.CharField(max_length=30)
    passport_validity = models.DateField
    birthday = models.DateField
    nationality = models.CharField(max_length=30)
    residence_country = models.CharField(max_length=30)
    residence_city = models.CharField(max_length=30)
    address = models.TextField()
    phone = models.CharField(max_length=30)
    email = models.EmailField
