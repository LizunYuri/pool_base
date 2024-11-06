from django.contrib import admin
from django.urls import include, path
from . import views




urlpatterns = [
    path('get-clients', views.get_clients, name='get-clients')
    ]
