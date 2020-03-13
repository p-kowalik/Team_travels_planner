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


class TicketForm(forms.Form):
    travel_booking_summary = forms.ModelChoiceField(queryset=TravelBookingSummary.objects.all())
    travel_date_start = forms.DateField()
    travel_date_end = forms.DateField()
    airport_departure = forms.ModelChoiceField(queryset=Airport.objects.all())
    airport_arrival = forms.ModelChoiceField(queryset=Airport.objects.all())
    ticket_cost = forms.DecimalField()
    supervisor_approval = forms.NullBooleanField()


class VisaForm(ModelForm):
    class Meta:
        model = Visa
        fields = '__all__'


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'


class HotelBookingForm(forms.Form):
    travel_booking_summary = forms.ModelChoiceField(queryset=TravelBookingSummary.objects.all())
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())
    check_in = forms.DateField()
    check_out = forms.DateField()


class TravelBookingSummaryForm(forms.Form):
    travel_calendar = forms.ModelChoiceField(queryset=TravelCalendar.objects.all())
    employee_comment = forms.CharField(label='Employee comment', max_length=500)
    supervisor_comment = forms.CharField(label='Supervisor comment', max_length=500)


class TravelCalendarForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
    travel_date_start = forms.DateField()
    travel_date_end = forms.DateField()
    city_from = forms.ModelChoiceField(queryset=City.objects.all())
    city_destination = forms.ModelChoiceField(queryset=City.objects.all())
    country_destination = forms.ModelChoiceField(queryset=Country.objects.all())
    employee_approval = forms.NullBooleanField()
    supervisor_approval = forms.NullBooleanField()
    notification_advance = forms.IntegerField(initial=7)
    travel_purpose_description = forms.CharField(max_length=500)


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")
