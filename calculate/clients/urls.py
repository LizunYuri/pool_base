from django.contrib import admin
from django.urls import include, path
from . import views




urlpatterns = [
    path('get-clients/', views.get_clients, name='get-clients'),
    path('clients_list/', views.clients_list, name='clients_list'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('client/<int:client_id>/delete/', views.delete_client, name='delete_client'),
    path('client/<int:client_id>/edit/', views.client_edit, name='client_edit'),
    path('create/', views.create_client, name='create_client'),
    path('search/', views.search_clients, name='search_client')
    ]
