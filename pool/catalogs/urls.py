from django.contrib import admin
from django.urls import path, include
from catalogs import views


urlpatterns = [
    path('export-filters/', views.export_filters, name='export_filters'),
    path('export-pumps/', views.export_pumps, name='export_pumps'),
    path('export-finished/', views.export_finished, name='export-finished'),
    path('export-zaclad/', views.export_zaklad, name='export-zaklad'),
    path('export-heating/', views.export_heating, name='export-heating'),

    path('update_filters/', views.update_filters, name='update_filters'),
    path('update_pumps/', views.update_pumps, name='update_pumps'),
    path('update_finished/', views.update_finished, name='update_finished'),

    path('logistic/', views.message_logistic, name='message_logistic'),
]