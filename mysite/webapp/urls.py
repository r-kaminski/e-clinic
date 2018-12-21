from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views


app_name = 'webapp'

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^login/$', auth_views.LoginView.as_view(template_name="register/login.html"), name='login'),
        url(r'^logout/$', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
        url(r'^register/$', views.register, name='register'),
        url(r'^search/$', views.search, name='search'),
        ]
