from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel, name='panel'),
    path('accountant-panel/', views.accountant_panel, name='accountant_panel')
]