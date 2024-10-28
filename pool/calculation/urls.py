from django.urls import path
from . import views

urlpatterns = [
    path('create-client/', views.create_client, name='create_client'),
    path('create-rectangle/', views.create_rectangle, name='create_rectangle'),


    path('get-materials/', views.get_materials, name='get_materials'),
    path('get-heating/', views.get_heating, name='get-heating'),
    path('get_desinfection/', views.get_desinfection, name='get_desinfection'),
    path('get_entrance/', views.get_entrance, name='get_entrance'),
    path('get_filtred_pumps/', views.get_filtred_pumps, name='get_filtred_pumps'),
    path('get_filtred_filter/', views.get_filtred_filter, name='get_filtred_filter'),
    path('get_skimmers/', views.get_skimmers, name='get_skimmers'),
    path('get_nozzle/', views.get_nozzle, name='get_nozzle'),
    path('get_bottom_drain/', views.get_bottom_drain, name='get_bottom_drain'),
    path('get_adding_water/', views.get_adding_water, name='get_adding_water'),
    path('get_vacuum_clean_nozzle/', views.get_vacuum_clean_nozzle, name='get_vacuum_clean_nozzle'),
    path('get_drain_nozzle/', views.get_drain_nozzle, name='drain_nozzle'),
    path('get_filter_valve/', views.get_filter_valve, name='get_filter_valve'),
    path('get_lighting/', views.get_lighting, name='get_lighting'),
    

    path('accept_size/', views.accept_size, name='accept_size'),
    path('accept_filter/', views.get_accept_filters, name='accept_filter'),
    path('get_accept_lighting/', views.get_accept_lighting, name='get_accept_lighting'),

    path('rectangle/<int:pk>/', views.rectangle_detail, name='rectangle_detail'),
]  