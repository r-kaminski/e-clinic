from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
import sys

# from django.db import connection

from .models import Clinic, Doctor, Address, Appointment, Data, Patient
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .forms import SignUpForm

from django.urls import reverse

import datetime

doctors_and_appointments_t = ()

specs = []
cities = []

def refresh_appointments():
    start_date = '2018-01-01'
    yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    Appointment.objects.filter(appointment_date__range=[start_date, yesterday_date]).delete()


def populate_doctors_and_appointments(appointments):
     doctors_and_appointments = {}
     for appointment in appointments:
         doctor = Doctor.objects.get(doctor_id=appointment.doctor_id)
         if doctor not in doctors_and_appointments.keys():
             tmp_list = []
             tmp_list.append(appointment)
             doctors_and_appointments[doctor] = tmp_list
         else:
             doctors_and_appointments[doctor].append(appointment)


     for doctor in doctors_and_appointments.keys():
         doctors_and_appointments[doctor].sort(key=lambda x: x.appointment_date)

     global doctors_and_appointments_t
     doctors_and_appointments_t = tuple(doctors_and_appointments.items())


def populate_appointments(request_copy):
    specialization = request_copy.POST.get('specialization', '')
    print("specialization inside populate_app:")
    print(specialization)
    if specialization:
        city = request_copy.POST.get('city', '')
        
        start_date = request_copy.POST.get('start_date', '2018-01-01')
        end_date = request_copy.POST.get('end_date', '2020-01-01')

        if not start_date:
            start_date = '2018-01-01'

        if not end_date:
            end_date = '2020-01-01'
        
        if city:
            appointments = Appointment.objects.filter(appointment_date__range=[start_date, end_date]).filter(doctor__specialization=specialization).filter(address__city=city)
        else:
            appointments = Appointment.objects.filter(appointment_date__range=[start_date, end_date]).filter(doctor__specialization=specialization)
    
    return appointments


def populate_specs_and_cities():
    global specs
    doctors = Doctor.objects.all()
    for doctor in doctors:
       spec = doctor.specialization
       if not spec in specs:
           specs.append(spec)

    global cities
    addresses = Address.objects.all()
    for address in addresses:
        city = address.city
        if not city in cities:
            cities.append(city)

def index(request):
    populate_specs_and_cities()

    if request.method == 'POST':
        if not request.POST.get('specialization', ''):
            return render(request, 'webapp/index.html', {'specs': specs, 'cities': cities, 'warning_no_specs': 'WARNING_NO_SPECS'})
        
        refresh_appointments()
        appointments = populate_appointments(request)
        if not appointments:
            return render(request, 'webapp/index.html', {'specs': specs, 'cities': cities, 'warning_no_apps': 'WARNING_NO_APPS'})
     
        populate_doctors_and_appointments(appointments)

        return HttpResponseRedirect(reverse('webapp:search')+"?page=1")
    else:
        return render(request, 'webapp/index.html', {'specs': specs, 'cities': cities})


def search(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment', '')
        appointment = Appointment.objects.get(appointment_id=appointment_id)

        user = request.user

        if user.profile.patient and appointment and not appointment.patient:
            appointment.patient = user.profile.patient
            appointment.save()
            return HttpResponseRedirect(reverse('webapp:view_appointments')+"?page=1")
     
    page_number = request.GET.get('page', 1)
    paginator = Paginator(doctors_and_appointments_t, 5)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return render(request, 'webapp/search.html', {'doctors_and_appointments': page, 'paginator': paginator})


def view_appointments(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id', '')
        appointment = Appointment.objects.get(appointment_id=appointment_id)
        appointment.patient = None
        appointment.save()
        return HttpResponseRedirect(reverse('webapp:view_appointments')+"?page=1")

    user = request.user
    appointments = Appointment.objects.filter(patient_id=user.profile.patient_id)
        
    appointments_and_doctors = {}
    for appointment in appointments:
        doctor = Doctor.objects.get(doctor_id=appointment.doctor_id)
        appointments_and_doctors[appointment] = doctor


    appointments_and_doctors_t = tuple(appointments_and_doctors.items())

    paginator = Paginator(appointments_and_doctors_t, 5)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return render(request, 'webapp/appointments.html', {'doctors_and_appointments': page, 'paginator': paginator})


def login(request):
    return render(request, 'register/login.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            telephone_number = form.cleaned_data.get('telephone_number')

            data = Data.objects.create(first_name=first_name, last_name=last_name, telephone_number=telephone_number, email=email)
            data.save()
            patient = Patient.objects.create(data=data)
            patient.save()

            # cursor = connection.cursor()
            # cursor.callproc('INSERT_PATIENT', [first_name, last_name, telephone_number, email,])
            # patient = Patient.objects.filter(data__first_name=first_name).filter(data__last_name=last_name).filter(data__email=email).filter(data__telephone_number=telephone_number)[0]
            
            user.refresh_from_db()
            user.profile.patient = patient
            user.save()

            user.profile.save()

            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
           
            #user.profile.save()
            
            populate_specs_and_cities()

            return render(request, 'webapp/index.html', {'specs': specs, 'cities': cities})

        else:
            print('Invalid registration input')
    else:
        form = SignUpForm()
    return render(request, 'webapp/register.html', {'form': form})
