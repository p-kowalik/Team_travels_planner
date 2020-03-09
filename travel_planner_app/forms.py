from django import forms
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = '__all__'


class AirportForm(ModelForm):
    class Meta:
        model = Airport
        fields = '__all__'


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'


class VisaForm(ModelForm):
    class Meta:
        model = Visa
        fields = '__all__'


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'


class HotelBookingForm(ModelForm):
    class Meta:
        model = HotelBooking
        fields = '__all__'


class TravelBookingSummaryForm(ModelForm):
    class Meta:
        model = TravelBookingSummary
        fields = '__all__'


class TravelCalendar(ModelForm):
    class Meta:
        model = TravelCalendar
        fields = '__all__'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
