from django import forms
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator, MinValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus import DatePickerInput


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
    travel_date_start = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
    travel_date_end = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
    airport_departure = forms.ModelChoiceField(queryset=Airport.objects.all())
    airport_arrival = forms.ModelChoiceField(queryset=Airport.objects.all())
    ticket_cost = forms.DecimalField(max_digits=7, decimal_places=2,  validators=[MinValueValidator(0.00)])
    supervisor_approval = forms.NullBooleanField()


class VisaForm(ModelForm):
    class Meta:
        model = Visa
        fields = '__all__'
        widgets = {
            'issued_on': DatePickerInput(),
        }


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'


class HotelBookingForm(forms.Form):
    travel_booking_summary = forms.ModelChoiceField(queryset=TravelBookingSummary.objects.all())
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())
    check_in = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
    check_out = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))


class TravelBookingSummaryForm(forms.Form):
    travel_calendar = forms.ModelChoiceField(queryset=TravelCalendar.objects.all().order_by('travel_date_start'))
    employee_comment = forms.CharField(label='Employee comment', max_length=500, initial='waiting for comment')
    supervisor_comment = forms.CharField(label='Supervisor comment', max_length=500, initial='waiting for comment')


class TravelCalendarForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('surname'))
    travel_date_start = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
    travel_date_end = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
    city_from = forms.ModelChoiceField(queryset=City.objects.all().order_by('country'))
    city_destination = forms.ModelChoiceField(queryset=City.objects.all().order_by('country'))
    country_destination = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'))
    employee_approval = forms.NullBooleanField(initial=False)
    supervisor_approval = forms.NullBooleanField(initial=False)
    notification_advance = forms.IntegerField(initial=7)
    travel_purpose_description = forms.CharField(max_length=500, initial='Work')


class SearchForTravelsForm(forms.Form):
    employee = forms.ModelChoiceField(required=False, queryset=Employee.objects.all().order_by('surname'))
    travel_date_from = forms.DateField(required=False, widget=DatePickerInput(format='%Y-%m-%d'))
    travel_date_to = forms.DateField(required=False, widget=DatePickerInput(format='%Y-%m-%d'))


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'passport_validity': DatePickerInput(),
            'birthday': DatePickerInput(),
        }


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")
