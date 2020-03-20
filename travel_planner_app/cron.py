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


def upcoming_travels():
    date_in_15_days = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
    travels_upcoming = TravelCalendar.objects.filter(travel_date_start=date_in_15_days)
    if travels_upcoming:
        subject = 'Upcoming travels to be managed'
        message = f' Some travels are starting on: {date_in_15_days} and may require your attention!' \
                  f'See following details: {travels_upcoming}.' \
                  f'Login to your account for more details: http://localhost:8000/login/'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['supervisortravels@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
