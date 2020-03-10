from django.views import View
from travel_planner_app.forms import *
from django.shortcuts import render, redirect
from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LandingPage(View):
    def get(self, request):
        return render(request, "menu.html")


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


