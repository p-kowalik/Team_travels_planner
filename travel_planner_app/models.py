from django.db import models


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
        return str(self.city) + str(" ") + str(self.name) + str(" ") + str(self.IATA_code)

class Ticket(models.Model):
    travel_booking_summary = models.ForeignKey('TravelBookingSummary', on_delete=models.CASCADE)
    travel_date_start = models.DateField()
    travel_date_end = models.DateField()
    airport_departure = models.CharField(max_length=64)
    airport_arrival = models.CharField(max_length=64)
    ticket_cost = models.DecimalField(max_digits=5, decimal_places=2)
    supervisor_approval = models.BooleanField(default=False)


class Visa(models.Model):
    travel_booking_summary = models.ForeignKey('TravelBookingSummary', on_delete=models.CASCADE)
    issued_on = models.DateField()
    validity_days = models.IntegerField()
    extension_option = models.NullBooleanField(default=False)
    visa_cost = models.DecimalField(max_digits=5, decimal_places=2)


class Hotel(models.Model):
    name = models.CharField(max_length=64)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=30, null=True)
    email = models.EmailField
    cost_per_night = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.city


class HotelBooking(models.Model):
    travel_booking_summary = models.ForeignKey('TravelBookingSummary', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    cost_per_stay = models.DecimalField(max_digits=5, decimal_places=2)




class TravelBookingSummary(models.Model):
    travel_calendar = models.ForeignKey('TravelCalendar', on_delete=models.CASCADE)
    employee_comment = models.TextField(null=True)
    supervisor_comment = models.TextField(null=True)

    def __str__(self):
        return self.travel_calendar

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




class Employee(models.Model):
    forename = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    passport_no = models.CharField(max_length=30)
    passport_validity = models.DateField
    birthday = models.DateField
    nationality = models.CharField(max_length=30)
    residence_country = models.CharField(max_length=30)
    residence_city = models.CharField(max_length=30)
    address = models.TextField()
    phone = models.CharField(max_length=30)
    email = models.EmailField()
