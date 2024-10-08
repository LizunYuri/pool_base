from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_rectangle, name='create_rectangle'),
    path('rectangle/<int:pk>/', views.rectangle_detail, name='rectangle_detail'),
]