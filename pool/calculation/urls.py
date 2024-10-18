from django.urls import path
from . import views

urlpatterns = [
    path('create-client/', views.create_client, name='create_client'),
    path('create-rectangle/', views.create_rectangle, name='create_rectangle'),
    path('get-materials/', views.get_materials, name='get_materials'),
    path('get-heating/', views.get_heating, name='get-heating'),
    path('get_desinfection/', views.get_desinfection, name='get_desinfection'),
    path('rectangle/<int:pk>/', views.rectangle_detail, name='rectangle_detail'),
]