from django.urls import include, path
from . import views



urlpatterns = [
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('403/', views.access_denied, name='access_denied')
]