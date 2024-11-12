from django.contrib import admin
from django.urls import include, path
from . import views




urlpatterns = [
    path('get-equipment/', views.get_equipment, name='get-equipment'),
    path('pumps_list/', views.pumps_list, name='pumps_list'),
    ]
