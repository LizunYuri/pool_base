from django.contrib import admin
from django.urls import path, include
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('main.urls')),
    path('export-filters/', views.export_filters, name='export_filters'),
    path('update_filters/', views.update_filters, name='update_filters'),
    path('export-pumps/', views.export_pumps, name='export_pumps'),
    path('update_pumps/', views.update_pumps, name='update_pumps'),
    path('logistic/', views.message_logistic, name='message_logistic'),
    path('calculation/', include('calculation.urls'))
]
