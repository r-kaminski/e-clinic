from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
import sys

from .models import Clinic
#from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm

# get_object_or_404() - get()
# get_list_or_404() - filter()

def index(request):
    return render(request, 'webapp/index.html')

def search(request):
    return render(request, 'webapp/search.html')


# ????
def login(request):
    return render(request, 'register/login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('is_valid() == true')
            form.save()
            username = form.cleaned_data.get('username')
            #first_name = form.cleaned_data.get('first_name')
            #last_name = form.cleaned_data.get('last_name')
            #email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return render(request, 'webapp/index.html')
        else:
            print('is_valid() == false')
    else:
        form = UserCreationForm()
    return render(request, 'webapp/register.html', {'form': form})
