"""travel_planner_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from travel_planner_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageLogin.as_view(), name="start"),
    path('index/', LandingPage.as_view(), name="landing-page"),


    path('main_menu/', MainMenu.as_view(), name="menu"),
    path('bookings_upcoming/', BookingsUpcoming.as_view(), name="bookings-upcoming"),
    path('booking_details/<int:id>/', BookingsUpcomingInfo.as_view(), name="bookings-upcoming-info"),
    path('manage_trips/', ManageTrips.as_view(), name="manage-trips"),
    path('manage_employees/', ManageEmployees.as_view(), name="manage-employees"),
    path('manage_locations/', ManageLocations.as_view(), name="manage-locations"),


    path('add_travel/', AddTravelCalendarView.as_view(), name="add-travel-calendar"),
    path('list_travel/', ListTravelCalendarView.as_view(), name="list-travel"),

    path('add_travel_booking_summary/', AddTravelBookingSummaryView.as_view(), name="add-travel-booking-summary"),
    path('list_travel_booking_summary/', ListTravelBookingSummaryView.as_view(), name="list-travel-booking-summary"),

    path('add_ticket/', AddTicketView.as_view(), name="add-ticket"),
    path('list_ticket/', ListTicketView.as_view(), name="list-ticket"),

    path('add_visa/', AddVisaView.as_view(), name="add-visa"),
    path('list_visa/', ListVisaView.as_view(), name="list-visa"),

    path('add_hotel_booking/', AddHotelBookingView.as_view(), name="add-hotel-booking"),
    path('list_hotel_booking/', ListHotelBookingView.as_view(), name="list-hotel-booking"),


    path('add_user/', AddUserView.as_view(), name="add-user"),
    path('list_user/', UsersList.as_view(), name="list-user"),
    path('update_user/<int:pk>/', UpdateUserView.as_view(template_name='update_user_form.html'), name="update-user"),
    path('delete_user/<int:id>/', DeleteUserView.as_view(), name="delete-user"),

    path('add_employee/', AddEmployeeView.as_view(), name="add-employee"),
    path('list_employee/', EmployeesList.as_view(), name="list-employee"),
    path('update_employee/<int:pk>/', UpdateEmployeeView.as_view(template_name='update_employee_form.html'), name="update-employee"),
    path('delete_employee/<int:id>/', DeleteEmployeeView.as_view(), name="delete-employee"),


    path('add_country/', AddCountryView.as_view(), name="add-country"),
    path('list_country/', CountryListView.as_view(), name="list-country"),
    path('country_delete/<int:id>/', DeleteCountryView.as_view(), name="delete-country"),

    path('add_city/', AddCityView.as_view(), name="add-city"),
    path('list_city/', CityListView.as_view(), name="list-city"),
    path('city_delete/<int:id>/', DeleteCityView.as_view(), name="delete-city"),

    path('add_airport/', AddAirportView.as_view(), name="add-airport"),
    path('list_airport/', AirportListView.as_view(), name="list-airport"),
    path('airport_delete/<int:id>/', DeleteAirportView.as_view(), name="delete-airport"),

    path('add_hotel/', AddHotelView.as_view(), name="add-hotel"),
    path('list_hotel/', HotelListView.as_view(), name="list-hotel"),
    path('hotel_delete/<int:id>/', DeleteHotelView.as_view(), name="delete-hotel"),


    path('accounts/', include('django.contrib.auth.urls')),
#    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='landing_page_login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='change-password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='change-password-done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
