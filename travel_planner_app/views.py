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
from django.contrib import messages

from django.core.mail import EmailMessage
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


#currentDate = datetime.now()


class LandingPage(View):
    def get(self, request):
        global currentdate
        currentDate = datetime.now()
        return render(request, "welcome.html", {"date": currentDate})


class LandingPageLogin(View):
    def get(self, request):
        return render(request, "landing_page_login.html")

    def post(self, request):
        if request.user.is_staff:
            print("hello")


class Base(LoginRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'add_country'

    def get(self, request):
        return render(request, "base.html")


class UsersRedirectingView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        staff = ['pawel', 'Supervisor', 'Coordinator']
        if request.user.get_username() in staff:
            return redirect('/index/')
        else:
            return redirect('/index_employee/')


class EmployeeLandingPageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user_id = self.request.user.id
        user_name = request.user.get_username()
        employee_logged = Employee.objects.get(user=user_id)
        travels = TravelCalendar.objects.filter(employee=employee_logged).order_by('travel_date_start')
        return render(request, "employee_welcome.html", {"user_id": user_id,
                                                         "employee_logged": employee_logged,
                                                         "travels": travels})


class EmployeeIndexPageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user_id = self.request.user.id
        user_name = request.user.get_username()
        employee_logged = Employee.objects.get(user=user_id)
        travels = TravelCalendar.objects.filter(employee=employee_logged).order_by('travel_date_start')
        return render(request, "employee_welcome.html", {"user_id": user_id,
                                                         "employee_logged": employee_logged,
                                                         "travels": travels})


class MainMenu(LoginRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        date_in_14_days = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        travel_details = TravelCalendar.objects.filter(travel_date_start__gt=date.today()).filter(travel_date_start__lt=date_in_14_days).order_by('travel_date_start')
#        print("tr_det: ", travel_details)
#       for travel_detail in travel_details:
#           travel_id = travel_detail.id
#           print("travel_id: ", travel_id)
#           try:
#               booking_details = TravelBookingSummary.objects.get(travel_calendar=travel_id)
#               booking_summary_id = booking_details.id
#               print("booking_summary_id: ", booking_summary_id)
#               employee_id = travel_detail.employee.id
#               print("emp id: ", employee_id)
#               employee_name = travel_detail.employee
#               print("emp name: ", employee_name)
#               employee_details = Employee.objects.get(id=employee_id)

#               ticket_details = Ticket.objects.get(travel_booking_summary=booking_summary_id)
#               print("ticket_details id: ", ticket_details.id)

#               hotel_booking_details = HotelBooking.objects.get(travel_booking_summary=booking_summary_id)
#               print("hotel_name id: ", hotel_booking_details.hotel)

#               hotel_id = hotel_booking_details.hotel.id
#               print("hotel id: ", hotel_id)
#               hotel_details = Hotel.objects.get(id=hotel_id)

#           except Exception:
#               #pass
#               continue

        return render(request, "bookings_upcoming_list.html", {"travel_details": travel_details,
                                                                   #"booking_details": booking_details,
                                                                    #"employee_details": employee_details,
                                                                     #"ticket_details": ticket_details,
                                                                     #"hotel_booking_details": hotel_booking_details,
                                                                     #"hotel_details": hotel_details,
                                                                 #"visa_details": visa_details
                                                               })


class BookingsUpcoming(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        bookings_list = TravelCalendar.objects.filter(travel_date_start__gt=date.today()).order_by('travel_date_start')
        form = SearchForTravelsForm()
        page = request.GET.get('page', 1)
        paginator = Paginator(bookings_list, 10)
        try:
            bookings = paginator.page(page)
        except PageNotAnInteger:
            bookings = paginator.page(1)
        except EmptyPage:
            bookings = paginator.page(paginator.num_pages)
        return render(request, "future_travels.html", {"bookings": bookings, 'form': form})


class SearchForTravelsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request):
        form = SearchForTravelsForm()
        return render(request, 'future_travels.html', {'form': form})

    def post(self, request):
        form = SearchForTravelsForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            travel_date_from = form.cleaned_data['travel_date_from']
            travel_date_to = form.cleaned_data['travel_date_to']
            if travel_date_from and travel_date_to:
                if travel_date_from > travel_date_to:
                    messages.error(request, 'Dates mismatch.')
                    return redirect('/bookings_upcoming/')
                    #messages.error(request, "Error")
                    #return (print('Date conflict'))
                    #raise Exception ('Travel start date cant be after departure')
            if not employee:
                if not travel_date_from and not travel_date_to:
                    return redirect('/bookings_upcoming/')
                elif not travel_date_from:
                    bookings = TravelCalendar.objects.filter(travel_date_start__gt='2000-01-01').filter(
                        travel_date_start__lt=travel_date_to).order_by('travel_date_start')
                elif not travel_date_to:
                    bookings = TravelCalendar.objects.filter(travel_date_start__gt=travel_date_from).filter(
                        travel_date_start__lt='2100-01-01').order_by('travel_date_start')
                else:
                    bookings = TravelCalendar.objects.filter(travel_date_start__gt=travel_date_from).filter(travel_date_start__lt=travel_date_to).order_by('travel_date_start')
            elif not travel_date_from and not travel_date_to:
                bookings = TravelCalendar.objects.filter(employee=employee).order_by('travel_date_start')
            elif not travel_date_from:
                bookings = TravelCalendar.objects.filter(employee=employee).filter(travel_date_start__gt='2000-01-01').filter(
                    travel_date_start__lt=travel_date_to).order_by('travel_date_start')
            elif not travel_date_to:
                bookings = TravelCalendar.objects.filter(employee=employee).filter(travel_date_start__gt=travel_date_from).filter(
                    travel_date_start__lt='2100-01-01').order_by('travel_date_start')
            else:
                bookings = TravelCalendar.objects.filter(employee=employee).filter(travel_date_start__gt=travel_date_from).filter(travel_date_start__lt=travel_date_to).order_by('travel_date_start')
            return render(request, "future_travels.html", {"bookings": bookings, 'form': form})


class BookingsUpcomingInfo(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
 #       try:
 #           travel_details = TravelCalendar.objects.get(id=id)
 #           travel_id = travel_details.id
 #           employee_id = travel_details.employee.id
 #           employee_name = travel_details.employee
 #           employee_details = Employee.objects.get(id=employee_id)
 #       except ObjectDoesNotExist:
 #           return render(request, "booking_upcoming_details.html", {"travel_details": travel_details,
 #                                                                    "employee_details": employee_details})
        try:
            travel_details = TravelCalendar.objects.get(id=id)
            travel_id = travel_details.id
            employee_id = travel_details.employee.id
            #employee_name = travel_details.employee
            employee_details = Employee.objects.get(id=employee_id)
            booking_details = TravelBookingSummary.objects.get(travel_calendar=travel_id)
            booking_summary_id = booking_details.id
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details.html", {"travel_details": travel_details,
                                                                     "employee_details": employee_details})
        try:
            employee_id = travel_details.employee.id
            employee_name = travel_details.employee
            employee_details = Employee.objects.get(id=employee_id)
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details.html", {"travel_details": travel_details,
                                                                     "booking_details": booking_details})
        try:
            ticket_details = Ticket.objects.get(travel_booking_summary=booking_summary_id)
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details.html", {"travel_details": travel_details,
                                                                     "booking_details": booking_details,
                                                                     "employee_details": employee_details})
        try:
            hotel_booking_details = HotelBooking.objects.get(travel_booking_summary=booking_summary_id)
            hotel_id = hotel_booking_details.hotel.id
            hotel_details = Hotel.objects.get(id=hotel_id)
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details.html", {"travel_details": travel_details,
                                                                     "booking_details": booking_details,
                                                                     "employee_details": employee_details,
                                                                     "ticket_details": ticket_details})
        try:
            visa_details = Visa.objects.get(travel_booking_summary=booking_summary_id)
            visa_id = visa_details.id
            print("visa_id: ", visa_id)
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details.html", {"travel_details": travel_details,
                                                                     "booking_details": booking_details,
                                                                     "employee_details": employee_details,
                                                                     "ticket_details": ticket_details})

        return render(request, "booking_upcoming_details.html", {"travel_details": travel_details,
                                                                 "booking_details": booking_details,
                                                                 "employee_details": employee_details,
                                                                 "ticket_details": ticket_details,
                                                                 "hotel_booking_details": hotel_booking_details,
                                                                 "hotel_details": hotel_details,
                                                                 "visa_details": visa_details})


class BookingsUpcomingEmployeeInfo(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        try:
            travel_details = TravelCalendar.objects.get(id=id)
            travel_id = travel_details.id
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details_employee.html", {"travel_details": travel_details})
        try:
            booking_details = TravelBookingSummary.objects.get(travel_calendar=travel_id)
            booking_summary_id = booking_details.id
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details_employee.html", {"travel_details": travel_details})
        try:
            employee_id = travel_details.employee.id
            employee_name = travel_details.employee
            employee_details = Employee.objects.get(id=employee_id)
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details_employee.html", {"travel_details": travel_details,
                                                                     "booking_details": booking_details})
        try:
            ticket_details = Ticket.objects.get(travel_booking_summary=booking_summary_id)
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details_employee.html", {"travel_details": travel_details,
                                                                     "booking_details": booking_details,
                                                                     "employee_details": employee_details})
        try:
            hotel_booking_details = HotelBooking.objects.get(travel_booking_summary=booking_summary_id)
            hotel_id = hotel_booking_details.hotel.id
            hotel_details = Hotel.objects.get(id=hotel_id)
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details_employee.html", {"travel_details": travel_details,
                                                                     "booking_details": booking_details,
                                                                     "employee_details": employee_details,
                                                                     "ticket_details": ticket_details})
        try:
            visa_details = Visa.objects.get(travel_booking_summary=booking_summary_id)
            visa_id = visa_details.id
            print("visa_id: ", visa_id)
        except ObjectDoesNotExist:
            return render(request, "booking_upcoming_details_employee.html", {"travel_details": travel_details,
                                                                     "booking_details": booking_details,
                                                                     "employee_details": employee_details,
                                                                     "ticket_details": ticket_details})

        return render(request, "booking_upcoming_details_employee.html", {"travel_details": travel_details,
                                                                 "booking_details": booking_details,
                                                                 "employee_details": employee_details,
                                                                 "ticket_details": ticket_details,
                                                                 "hotel_booking_details": hotel_booking_details,
                                                                 "hotel_details": hotel_details,
                                                                 "visa_details": visa_details})


class BookingsUpcomingEmployeeApprove(LoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = TravelCalendar
    fields = ('employee_approval',)

    success_url = '/employee_travels/'


class BookingsUpcomingEmployeeComment(LoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = TravelBookingSummary
    fields = ('employee_comment',)

    success_url = '/employee_travels/'
#    user_id = self.request.user.id
#    user_name = request.user.get_username()
#    employee_logged = Employee.objects.get(user=user_id)
#    travels = TravelCalendar.objects.filter(employee=employee_logged).order_by('travel_date_start')
#    return render(request, "employee_welcome.html", {"user_id": user_id,
#                                                     "employee_logged": employee_logged,
#                                                     "travels": travels})


# update employee information by employee
class UpdateEmployeeByEmployeeView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = Employee
    fields = ('passport_no', 'passport_validity', 'residence_country', 'residence_city', 'address', 'phone', 'email')
    success_url = '/index_employee/'


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
            t = TravelCalendar.objects.create(
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
            employeee = Employee.objects.get(id=t.employee.id)
            print("emp name: ", employeee)
            employeee_id = t.employee.id
            print("emp id: ", employeee_id)
            employeee_email = employeee.email
            print("employeee_email: ", employeee_email)
            subject = 'New travel added'
            message = ' Please login to your account http://localhost:8000/login/,' \
                      ' to see recently scheduled travel. '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [employeee_email, 'supervisortravels@gmail.com']
            send_mail(subject, message, email_from, recipient_list)
            return redirect('/main_menu/')
        return render(request, 'add_travel_calendar_form.html', {'form': form})


# travel calendar - all
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


# travel calendar - employee
class ListEmployeeTravelCalendarView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user_id = self.request.user.id
        print("user_id", user_id)
        user_name = request.user.get_username()
        print("username: ", user_name)
        employee_logged = Employee.objects.get(user=user_id)
#        employee_id = employee.id
#        employee_travels_list = TravelCalendar.objects.filter(employee.id=employee_id).order_by('travel_date_start')
        travels = TravelCalendar.objects.filter(employee=employee_logged).order_by('travel_date_start')
        print("travels: ", travels)
        print("id: ", travels)
        bookings = {}
        for travel in travels:
            travel_id = travel.id
            print("travel :", travel.id)
            try:
                booking = TravelBookingSummary.objects.get(travel_calendar=travel_id)
                bookings.update({travel.id: booking.employee_comment})
                #bookings.append(booking.employee_comment)
                booking_id = booking.id
#                bookings.append(booking_id)
                employee_comment = booking.employee_comment
                supervisor_comment = booking.supervisor_comment
                print("booking id: ", booking_id)
                print("employee_comment : ", employee_comment)
                print("supervisor_comment : ", supervisor_comment)
            except ObjectDoesNotExist:
                continue
        print("bookings :", bookings)
        return render(request, "employee_travel_calendar_list.html", {"user_id": user_id,
                                                                      "employee_logged": employee_logged,
                                                                      "travels": travels,
                                                                      "employee_comment": employee_comment,
                                                                      "bookings": bookings})



# delete travel calendar
class DeleteTravelCalendarView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        travel_calendar_to_delete = TravelCalendar.objects.get(id=id)
        travel_calendar_to_delete.delete()
        return redirect('/manage_trips/')


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
            tb = TravelBookingSummary.objects.create(
                travel_calendar=form.cleaned_data['travel_calendar'],
                employee_comment=form.cleaned_data['employee_comment'],
                supervisor_comment=form.cleaned_data['supervisor_comment'])
            travel_calend = TravelCalendar.objects.get(employee=tb.travel_calendar.employee)
            employeee = Employee.objects.get(id=travel_calend.employee.id)
            employeee_email = employeee.email
            subject = 'New booking created'
            message = ' Please login to your account http://localhost:8000/login/,' \
                      ' to follow bookings related to scheduled travel. '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [employeee_email, 'supervisortravels@gmail.com']
            send_mail(subject, message, email_from, recipient_list)
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


# delete travel booking summary
class DeleteTravelBookingSummaryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        travel_booking_summary_to_delete = TravelBookingSummary.objects.get(id=id)
        travel_booking_summary_to_delete.delete()
        return redirect('/manage_trips/')


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
            return redirect('/list_ticket/')
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


# delete ticket
class DeleteTicketsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        tickets_to_delete = Ticket.objects.get(id=id)
        tickets_to_delete.delete()
        return redirect('/manage_trips/')


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
            return redirect('/manage_trips/')
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


# delete visa
class DeleteVisaView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        Visa_to_delete = Visa.objects.get(id=id)
        Visa_to_delete.delete()
        return redirect('/manage_trips/')


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
            return redirect('/manage_trips/')
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


# delete hotel booking
class DeleteHotelBookingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'view_user'

    def get(self, request, id):
        employee_to_delete = HotelBooking.objects.get(id=id)
        employee_to_delete.delete()
        return redirect('/manage_trips/')


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
        employees_list = Employee.objects.all().order_by('surname')
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
            return redirect('/list_airport/')
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
        airport_to_delete = Airport.objects.get(id=id)
        airport_to_delete.delete()
        return redirect('/list_airport/')


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


