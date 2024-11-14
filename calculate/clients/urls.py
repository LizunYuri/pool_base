from django.contrib import admin
from django.urls import include, path
from . import views




urlpatterns = [
    path('get-clients/', views.get_clients, name='get-clients'),
    path('clients_list/', views.clients_list, name='clients-list'),
    path('client/<int:client_id>/', views.client_detail, name='client-detail'),
    path('client/<int:client_id>/delete/', views.delete_client, name='delete-client'),
    path('client/<int:client_id>/edit/', views.client_edit, name='client_edit'),
    path('create/', views.create_client, name='create-client'),
    path('search/', views.search_clients, name='search-client')
    ]
