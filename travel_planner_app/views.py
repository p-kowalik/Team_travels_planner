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
    send_mail( subject, message, email_from, recipient_list )
    return redirect('base/')


class LandingPage(View):
    def get(self, request):
        return render(request, "landing_page.html")


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
        bookings = TravelCalendar.objects.filter(travel_date_start__gt=date.today()).filter(travel_date_start__lt=date_in_14_days)
        return render(request, "menu.html", {"bookings": bookings})


class BookingsUpcoming(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        bookings = TravelCalendar.objects.filter(travel_date_start__gt=date.today())
        return render(request, "future_travels.html", {"bookings": bookings})


class ManageTrips(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        return render(request, "trips.html")


class ManageEmployees(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        return render(request, "employees_users.html")


class ManageLocations(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'view_user'
    login_url = '/login/'

    def get(self, request):
        return render(request, "locations.html")


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


class EmployeesList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        employees = Employee.objects.all()
        return render(request, "employees_list.html", {"employees": employees})


class UpdateEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    permission_required = 'view_user'

    model = Employee
    fields = ('id', 'forename', 'surname', 'passport_no', 'passport_validity', 'birthday', 'nationality',
              'residence_country', 'residence_city', 'address', 'phone', 'email', 'user')
    success_url = '/main_menu/'


#class UpdateEmployeeView(LoginRequiredMixin, View):
#   login_url = '/login/'

#   def get(self, request, id):
#       form = EmployeeForm()
#       return render(request, 'update_employee_form.html', {'form': form})

#   def post(self, request, id):
#       form = EmployeeForm(request.POST)
#       if form.is_valid():
#           employee_update = Employee.objects.get(id=id)
#           employee_update.forename = form.cleaned_data['forename']
#           employee_update.surname = form.cleaned_data['surname']
#           employee_update.passport_no = form.cleaned_data['passport_no']
#           employee_update.passport_validity = form.cleaned_data['passport_validity']
#           employee_update.birthday = form.cleaned_data['birthday']
#           employee_update.nationality = form.cleaned_data['nationality']
#           employee_update.residence_country = form.cleaned_data['residence_country']
#           employee_update.residence_city = form.cleaned_data['residence_city']
#           employee_update.address = form.cleaned_data['address']
#           employee_update.phone = form.cleaned_data['phone']
#           employee_update.email = form.cleaned_data['email']
#           employee_update.user = form.cleaned_data['user']
#           employee_update.save()
#           return redirect('/main_menu/')
#       else:
#           return HttpResponse("Something went wrong")


class DeleteEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        employee_to_delete = Employee.objects.get(id=id)
        employee_to_delete.delete()
        return redirect('/main_menu/')


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


class UsersList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        users = User.objects.all()
        return render(request, "users_list.html", {"users": users})


class UpdateUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    permission_required = 'view_user'

    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'email')
    success_url = '/main_menu/'


#class UpdateUserView(LoginRequiredMixin, View):
#    login_url = '/login/'
#    def get(self, request, id):
#        form = AddUserForm()
#        return render(request, 'update_user_form.html', {'form': form})
#
#    def post(self, request, id):
#        form = AddUserForm(request.POST)
#        if form.is_valid():
#            user_update = User.objects.get(id=id)
#            user_update.forename = form.cleaned_data['forename']
#            user_update.surname = form.cleaned_data['surname']
#            user_update.passport_no = form.cleaned_data['passport_no']
#            user_update.passport_validity = form.cleaned_data['passport_validity']
#            user_update.birthday = form.cleaned_data['birthday']
#            user_update.save()
#            return redirect('/main_menu/')
#        else:
#            return HttpResponse("Something went wrong")


class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        user_to_delete = User.objects.get(id=id)
        user_to_delete.delete()
        return redirect('/main_menu/')


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

