from django.views import View
from travel_planner_app.forms import *
from django.shortcuts import render, redirect
#email configuration imports
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, datetime, timedelta

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


def email_new_country(request):
    subject = 'Dodano kraj'
    message = ' Witaj, dodano nowy kraj. Zaloguj sie aby potwierdzić. http://127.0.0.1:8000/add_country/ '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['pawel.mariusz.kowalik@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('main_menu/')


class LandingPage(View):
    def get(self, request):
        return render(request, "landing_page.html")


class Base(View):
    def get(self, request):
        return render(request, "base.html")


class MainMenu(View):
    def get(self, request):
        date_in_14_days = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        bookings = TravelCalendar.objects.filter(travel_date_start__gt=date.today()).filter(travel_date_start__lt=date_in_14_days)
        return render(request, "menu.html", {"bookings": bookings})


class BookingsUpcoming(View):
    def get(self, request):
        bookings = TravelCalendar.objects.filter(travel_date_start__gt=date.today())
        return render(request, "future_travels.html", {"bookings": bookings})


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
            email_new_country(request)
            return redirect('/main_menu/')
        return render(request, 'country_form.html', {'form': form})


class AddCityView(View):
    def get(self, request):
        form = CityForm()
        return render(request, 'city_form.html', {'form': form})

    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
        return render(request, 'city_form.html', {'form': form})


class AddAirportView(View):
    def get(self, request):
        form = AirportForm()
        return render(request, 'add_airport_form.html', {'form': form})

    def post(self, request):
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
        return render(request, 'add_airport_form.html', {'form': form})


class AddVisaView(View):
    def get(self, request):
        form = VisaForm()
        return render(request, 'add_visa_form.html', {'form': form})

    def post(self, request):
        form = VisaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
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
            return redirect('/main_menu/')
        return render(request, 'add_employee_form.html', {'form': form})


class AddTicketView(View):
    def get(self, request):
        form = TicketForm()
        return render(request, 'add_ticket_form.html', {'form': form})

    def post(self, request):
        form = TicketForm(request.POST)
        if form.is_valid():
            Ticket.objects.create(
                travel_booking_summary=form.cleaned_data['travel_booking_summary'],
                travel_date_start=form.cleaned_data['travel_date_start'],
                travel_date_end=form.cleaned_data['travel_date_end'],
                airport_departure=form.cleaned_data['airport_departure'],
                airport_arrival=form.cleaned_data['airport_arrival'],
                ticket_cost=form.cleaned_data['ticket_cost'],
                supervisor_approval=form.cleaned_data['supervisor_approval'])
            return redirect('/main_menu/')
        return render(request, 'add_employee_form.html', {'form': form})


class AddHotelBookingView(View):
    def get(self, request):
        form = HotelBookingForm()
        return render(request, 'add_hotel_booking_form.html', {'form': form})

    def post(self, request):
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            HotelBooking.objects.create(
                travel_booking_summary=form.cleaned_data['travel_booking_summary'],
                hotel=form.cleaned_data['hotel'],
                check_in=form.cleaned_data['check_in'],
                check_out=form.cleaned_data['check_out'])
            return redirect('/main_menu/')
        return render(request, 'add_hotel_booking_form.html', {'form': form})


class AddTravelBookingSummaryView(View):
    def get(self, request):
        form = TravelBookingSummaryForm()
        return render(request, 'add_travel_booking_summary_form.html', {'form': form})

    def post(self, request):
        form = TravelBookingSummaryForm(request.POST)
        if form.is_valid():
            TravelBookingSummary.objects.create(
                travel_calendar=form.cleaned_data['travel_calendar'],
                employee_comment=form.cleaned_data['employee_comment'],
                supervisor_comment=form.cleaned_data['supervisor_comment'])
            return redirect('/main_menu/')
        return render(request, 'add_travel_booking_summary_form.html', {'form': form})


class AddTravelCalendarView(View):
    def get(self, request):
        form = TravelCalendarForm()
        return render(request, 'add_travel_calendar_form.html', {'form': form})

    def post(self, request):
        form = TravelCalendarForm(request.POST)
        if form.is_valid():
            TravelCalendar.objects.create(
                employee=form.cleaned_data['employee'],
                travel_date_start=form.cleaned_data['travel_date_start'],
                travel_date_end=form.cleaned_data['travel_date_end'],
                city_from=form.cleaned_data['city_from'],
                city_destination=form.cleaned_data['city_destination'],
                country_destination=form.cleaned_data['country_destination'],
                employee_approval=form.cleaned_data['employee_approval'],
                supervisor_approval=form.cleaned_data['supervisor_approval'],
                notification_advance=form.cleaned_data['notification_advance'],
                travel_purpose_description=form.cleaned_data['travel_purpose_description'],)
            return redirect('/main_menu/')
        return render(request, 'add_travel_calendar_form.html', {'form': form})

