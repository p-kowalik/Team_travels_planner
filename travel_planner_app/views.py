from django.views import View
from travel_planner_app.forms import *
from django.shortcuts import render, redirect
#email configuration imports
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings

from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def email(request):
    subject = 'test email'
    message = ' django can do it '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['pawel.mariusz.kowalik@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('base/')


class LandingPage(View):
    def get(self, request):
        return render(request, "landing_page.html")


class Base(View):
    def get(self, request):
        return render(request, "base.html")


class MainMenu(View):
    def get(self, request):
        return render(request, "menu.html")


class ManageTrips(View):
    def get(self, request):
        return render(request, "trips.html")


class ManageEmployees(View):
    def get(self, request):
        return render(request, "employees_users.html")


class ManageLocations(View):
    def get(self, request):
        return render(request, "locations.html")


class AddCountryView(View):
    def get(self, request):
        form = CountryForm()
        return render(request, 'country_form.html', {'form': form})

    def post(self, request):
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'country_form.html', {'form': form})


class AddCityView(View):
    def get(self, request):
        form = CityForm()
        return render(request, 'city_form.html', {'form': form})

    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'city_form.html', {'form': form})


class AddAirportView(View):
    def get(self, request):
        form = AirportForm()
        return render(request, 'add_airport_form.html', {'form': form})

    def post(self, request):
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'add_airport_form.html', {'form': form})


class AddVisaView(View):
    def get(self, request):
        form = VisaForm()
        return render(request, 'add_visa_form.html', {'form': form})

    def post(self, request):
        form = VisaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'add_visa_form.html', {'form': form})


class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'add_user_form.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'add_user_form.html', {'form': form})


class AddEmployeeView(View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, 'add_employee_form.html', {'form': form})

    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'add_employee_form.html', {'form': form})


class AddTicketView(View):
    def get(self, request):
        form = TicketForm()
        return render(request, 'add_ticket_form.html', {'form': form})

    def post(self, request):
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'add_employee_form.html', {'form': form})


class AddHotelBookingView(View):
    def get(self, request):
        form = HotelBookingForm()
        return render(request, 'add_hotel_booking_form.html', {'form': form})

    def post(self, request):
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'add_hotel_booking_form.html', {'form': form})


class AddTravelBookingSummaryView(View):
    def get(self, request):
        form = TravelBookingSummaryForm()
        return render(request, 'add_travel_booking_summary_form.html', {'form': form})

    def post(self, request):
        form = TravelBookingSummaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'add_travel_booking_summary_form.html', {'form': form})


class AddTravelCalendarView(View):
    def get(self, request):
        form = TravelCalendarForm()
        return render(request, 'add_travel_calendar_form.html', {'form': form})

    def post(self, request):
        form = TravelCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'add_travel_calendar_form.html', {'form': form})