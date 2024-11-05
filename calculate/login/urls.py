from django.urls import include, path
from . import views



urlpatterns = [
    path('', views.custom_login_view, name='sing_up')
]
