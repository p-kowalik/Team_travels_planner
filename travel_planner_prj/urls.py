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
    path('', LandingPage.as_view(), name="start"),
    path('boot', LandingPageBootstrap.as_view(), name="startBoot"),

    path('base/', Base.as_view(), name="base"),
    path('main_menu/', MainMenu.as_view(), name="menu"),
    path('bookings_upcoming/', BookingsUpcoming.as_view(), name="bookings-upcoming"),
    path('manage_trips/', ManageTrips.as_view(), name="manage-trips"),
    path('manage_employees/', ManageEmployees.as_view(), name="manage-employees"),
    path('manage_locations/', ManageLocations.as_view(), name="manage-locations"),

    path('add_user/', AddUserView.as_view(), name="add-user"),
    path('list_user/', UsersList.as_view(), name="list-user"),
    path('update_user/<int:pk>/', UpdateUserView.as_view(template_name='update_user_form.html'), name="update-user"),
    path('delete_user/<int:id>/', DeleteUserView.as_view(), name="delete-user"),

    path('add_employee/', AddEmployeeView.as_view(), name="add-employee"),
    path('list_employee/', EmployeesList.as_view(), name="list-employee"),
    path('update_employee/<int:pk>/', UpdateEmployeeView.as_view(template_name='update_employee_form.html'), name="update-employee"),
    path('delete_employee/<int:id>/', DeleteEmployeeView.as_view(), name="delete-employee"),

    path('add_country/', AddCountryView.as_view(), name="add-country"),
    path('add_city/', AddCityView.as_view(), name="add-city"),
    path('add_airport/', AddAirportView.as_view(), name="add-airport"),

    path('add_visa/', AddVisaView.as_view(), name="add-visa"),
    path('add_ticket/', AddTicketView.as_view(), name="add-ticket"),
    path('add_hotel_booking/', AddHotelBookingView.as_view(), name="add-hotel-booking"),
    path('add_travel_booking_summary/', AddTravelBookingSummaryView.as_view(), name="add-travel-booking-summary"),
    path('add_travel/', AddTravelCalendarView.as_view(), name="add-travel-calendar"),

    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='change-password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='change-password-done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
