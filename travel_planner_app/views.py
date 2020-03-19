from django.views import View
from django.http import HttpResponse
from travel_planner_app.forms import *
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, datetime, timedelta
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import EmailMessage
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


def email_new_travel_booking(request):
    subject = 'New travel plan created'
    message = ' Please login to your account http://localhost:8000/login/,' \
              ' review and approve/reject new plan for your travel. '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['travel.planner.employee1@onet.pl', 'supervisortravels@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    return redirect('base/')


def email_new_booking_summary(request):
    subject = 'New booking summary created'
    message = ' Please login to your account http://localhost:8000/login/,' \
              ' review and leave your comments. '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['travel.planner.employee1@onet.pl', 'supervisortravels@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    return redirect('base/')


class LandingPage(View):
    def get(self, request):
        return render(request, "welcome.html")


class LandingPageLogin(View):
    def get(self, request):
        return render(request, "landing_page_login.html")


class Base(LoginRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'add_country'

    def get(self, request):
        return render(request, "base.html")


class MainMenu(LoginRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        date_in_14_days = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        travel_details = TravelCalendar.objects.filter(travel_date_start__gt=date.today()).filter(travel_date_start__lt=date_in_14_days).order_by('travel_date_start')
        print("tr_det: ", travel_details)
        for travel_detail in travel_details:
            travel_id = travel_detail.id
            print("travel_id: ", travel_id)
            try:
                booking_details = TravelBookingSummary.objects.get(travel_calendar=travel_id)
                booking_summary_id = booking_details.id
                print("booking_summary_id: ", booking_summary_id)
                employee_id = travel_detail.employee.id
                print("emp id: ", employee_id)
                employee_name = travel_detail.employee
                print("emp name: ", employee_name)
                employee_details = Employee.objects.get(id=employee_id)
                ticket_details = Ticket.objects.get(travel_booking_summary=booking_summary_id)
                print("ticket_details id: ", ticket_details.id)
                hotel_booking_details = HotelBooking.objects.get(travel_booking_summary=booking_summary_id)
                print("hotel_name id: ", hotel_booking_details.hotel)
                hotel_id = hotel_booking_details.hotel.id
                print("hotel id: ", hotel_id)
                hotel_details = Hotel.objects.get(id=hotel_id)
            except Exception:
                #pass
                continue

        return render(request, "bookings_upcoming_list.html", {"travel_details": travel_details,
                                                                    "booking_details": booking_details,
                                                                    "employee_details": employee_details,
                                                                     "ticket_details": ticket_details,
                                                                     "hotel_booking_details": hotel_booking_details,
                                                                     "hotel_details": hotel_details})


class BookingsUpcoming(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        bookings_list = TravelCalendar.objects.filter(travel_date_start__gt=date.today()).order_by('travel_date_start')
        page = request.GET.get('page', 1)
        paginator = Paginator(bookings_list, 10)
        try:
            bookings = paginator.page(page)
        except PageNotAnInteger:
            bookings = paginator.page(1)
        except EmptyPage:
            bookings = paginator.page(paginator.num_pages)
        return render(request, "future_travels.html", {"bookings": bookings})


class BookingsUpcomingInfo(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        try:
            travel_details = TravelCalendar.objects.get(id=id)
            travel_id = travel_details.id
            booking_details = TravelBookingSummary.objects.get(travel_calendar=travel_id)
            booking_summary_id = booking_details.id
            print("booking_summary_id: ", booking_summary_id)
            employee_id = travel_details.employee.id
            print("emp id: ", employee_id)
            employee_name = travel_details.employee
            print("emp name: ", employee_name)
            employee_details = Employee.objects.get(id=employee_id)
            ticket_details = Ticket.objects.get(travel_booking_summary=booking_summary_id)
            print("ticket_details id: ", ticket_details.airport_departure)
            hotel_booking_details = HotelBooking.objects.get(travel_booking_summary=booking_summary_id)
            print("hotel_name id: ", hotel_booking_details.hotel)
            hotel_id = hotel_booking_details.hotel.id
            print("hotel id: ", hotel_id)
            hotel_details = Hotel.objects.get(id=hotel_id)



            return render(request, "booking_upcoming_details.html", {"travel_details": travel_details,
                                                                    "booking_details": booking_details,
                                                                    "employee_details": employee_details,
                                                                     "ticket_details": ticket_details,
                                                                     "hotel_booking_details": hotel_booking_details,
                                                                     "hotel_details": hotel_details})
        except ObjectDoesNotExist:
            return render(request, "add_travel_booking_summary_form.html")



# Travels management
# travel management menu
class ManageTrips(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        return render(request, "trips.html")


# add travel calendar
class AddTravelCalendarView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        form = TravelCalendarForm()
        return render(request, 'add_travel_calendar_form.html', {'form': form})

    def post(self, request):
        form = TravelCalendarForm(request.POST)
        if form.is_valid():
            email_new_travel_booking(request)
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


# travel calendar
class ListTravelCalendarView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        travels_list = TravelCalendar.objects.order_by('travel_date_start')
        page = request.GET.get('page', 1)
        paginator = Paginator(travels_list, 10)
        try:
            travels = paginator.page(page)
        except PageNotAnInteger:
            travels = paginator.page(1)
        except EmptyPage:
            travels = paginator.page(paginator.num_pages)
        return render(request, "travel_calendar_list.html", {"travels": travels})


# add travel booking summary
class AddTravelBookingSummaryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        form = TravelBookingSummaryForm()
        return render(request, 'add_travel_booking_summary_form.html', {'form': form})

    def post(self, request):
        form = TravelBookingSummaryForm(request.POST)
        if form.is_valid():
            email_new_booking_summary(request)
            TravelBookingSummary.objects.create(
                travel_calendar=form.cleaned_data['travel_calendar'],
                employee_comment=form.cleaned_data['employee_comment'],
                supervisor_comment=form.cleaned_data['supervisor_comment'])
            return redirect('/main_menu/')
        return render(request, 'add_travel_booking_summary_form.html', {'form': form})


# view travel booking summary
class ListTravelBookingSummaryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        travel_booking_summary_list = TravelBookingSummary.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(travel_booking_summary_list, 10)
        try:
            travel_booking_summary = paginator.page(page)
        except PageNotAnInteger:
            travel_booking_summary = paginator.page(1)
        except EmptyPage:
            travel_booking_summary = paginator.page(paginator.num_pages)
        return render(request, "travel_booking_summary_list.html", {"travel_booking_summary": travel_booking_summary})


# add ticket
class AddTicketView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

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


# view all tickets
class ListTicketView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        tickets_list = Ticket.objects.order_by('travel_date_start')
        page = request.GET.get('page', 1)
        paginator = Paginator(tickets_list, 10)
        try:
            tickets = paginator.page(page)
        except PageNotAnInteger:
            tickets = paginator.page(1)
        except EmptyPage:
            tickets = paginator.page(paginator.num_pages)
        return render(request, "ticket_list.html", {"tickets": tickets})


# add visa
class AddVisaView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        form = VisaForm()
        return render(request, 'add_visa_form.html', {'form': form})

    def post(self, request):
        form = VisaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
        return render(request, 'add_visa_form.html', {'form': form})


# view all visas
class ListVisaView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        visas_list = Visa.objects.order_by('travel_booking_summary')
        page = request.GET.get('page', 1)
        paginator = Paginator(visas_list, 10)
        try:
            visas = paginator.page(page)
        except PageNotAnInteger:
            visas = paginator.page(1)
        except EmptyPage:
            visas = paginator.page(paginator.num_pages)
        return render(request, "visa_list.html", {"visas": visas})


# add hotel bookings
class AddHotelBookingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

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


# view all hotel bookings
class ListHotelBookingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        hotel_booking_list = HotelBooking.objects.order_by('check_in')
        page = request.GET.get('page', 1)
        paginator = Paginator(hotel_booking_list, 10)
        try:
            hotel_bookings = paginator.page(page)
        except PageNotAnInteger:
            hotel_bookings = paginator.page(1)
        except EmptyPage:
            hotel_bookings = paginator.page(paginator.num_pages)
        return render(request, "hotel_bookings_list.html", {"hotel_bookings": hotel_bookings})


# Manage employees and users
# employees management menu
class ManageEmployees(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        return render(request, "employees_users.html")


# add employee
class AddEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        form = EmployeeForm()
        return render(request, 'add_employee_form.html', {'form': form})

    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
        return render(request, 'add_employee_form.html', {'form': form})


# list of employees
class EmployeesList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        employees_list = Employee.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(employees_list, 10)
        try:
            employees = paginator.page(page)
        except PageNotAnInteger:
            employees = paginator.page(1)
        except EmptyPage:
            employees = paginator.page(paginator.num_pages)
        return render(request, "employees_list.html", {"employees": employees})


# update employee information
class UpdateEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    permission_required = 'view_user'

    model = Employee
    fields = ('id', 'forename', 'surname', 'passport_no', 'passport_validity', 'birthday', 'nationality',
              'residence_country', 'residence_city', 'address', 'phone', 'email', 'user')
    success_url = '/main_menu/'


# delete employee
class DeleteEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        employee_to_delete = Employee.objects.get(id=id)
        employee_to_delete.delete()
        return redirect('/main_menu/')


# add user
class AddUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        form = AddUserForm()
        return render(request, 'add_user_form.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
        return render(request, 'add_user_form.html', {'form': form})


# users list
class UsersList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        users = User.objects.all()
        return render(request, "users_list.html", {"users": users})


# update user information
class UpdateUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    permission_required = 'view_user'

    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'email')
    success_url = '/main_menu/'


# delete users
class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        user_to_delete = User.objects.get(id=id)
        user_to_delete.delete()
        return redirect('/main_menu/')


# Mange locations
# locations menu
class ManageLocations(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'view_user'
    login_url = '/login/'

    def get(self, request):
        return render(request, "locations.html")


# add country
class AddCountryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'view_user'
    login_url = '/login/'

    def get(self, request):
        form = CountryForm()
        return render(request, 'country_form.html', {'form': form})

    def post(self, request):
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
        return render(request, 'country_form.html', {'form': form})


# list of countries
class CountryListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        countries_list = Country.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(countries_list, 20)
        try:
            countries = paginator.page(page)
        except PageNotAnInteger:
            countries = paginator.page(1)
        except EmptyPage:
            countries = paginator.page(paginator.num_pages)
        return render(request, "countries_list.html", {"countries": countries})


# delete country
class DeleteCountryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        country_to_delete = Country.objects.get(id=id)
        country_to_delete.delete()
        return redirect('/list_country/')


# add city
class AddCityView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        form = CityForm()
        return render(request, 'city_form.html', {'form': form})

    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
        return render(request, 'city_form.html', {'form': form})


# list of cities
class CityListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        cities_list = City.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(cities_list, 20)
        try:
            cities = paginator.page(page)
        except PageNotAnInteger:
            cities = paginator.page(1)
        except EmptyPage:
            cities = paginator.page(paginator.num_pages)
        return render(request, "cities_list.html", {"cities": cities})


# delete city
class DeleteCityView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        city_to_delete = City.objects.get(id=id)
        city_to_delete.delete()
        return redirect('/main_menu/')


# add airport
class AddAirportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        form = AirportForm()
        return render(request, 'add_airport_form.html', {'form': form})

    def post(self, request):
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
        return render(request, 'add_airport_form.html', {'form': form})


# list of airports
class AirportListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        airport_list = Airport.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(airport_list, 20)
        try:
            airports = paginator.page(page)
        except PageNotAnInteger:
            airports = paginator.page(1)
        except EmptyPage:
            airports = paginator.page(paginator.num_pages)
        return render(request, "airports_list.html", {"airports": airports})


# delete airport
class DeleteAirportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        employee_to_delete = Employee.objects.get(id=id)
        employee_to_delete.delete()
        return redirect('/main_menu/')


# add hotel
class AddHotelView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        form = HotelForm()
        return render(request, 'add_hotel_form.html', {'form': form})

    def post(self, request):
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/main_menu/')
        return render(request, 'add_hotel_form.html', {'form': form})


# list of hotel
class HotelListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        hotels_list = Hotel.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(hotels_list, 20)
        try:
            hotels = paginator.page(page)
        except PageNotAnInteger:
            hotels = paginator.page(1)
        except EmptyPage:
            hotels = paginator.page(paginator.num_pages)
        return render(request, "hotels_list.html", {"hotels": hotels})


# delete hotel
class DeleteHotelView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        hotel_to_delete = Hotel.objects.get(id=id)
        hotel_to_delete.delete()
        return redirect('/main_menu/')