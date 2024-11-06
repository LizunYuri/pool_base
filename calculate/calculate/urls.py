
from django.contrib import admin
from django.urls import include, path
from login import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls'), name='login'),
    path('panel/', include('panel.urls'), name='admin'),
    path('clients/', include('clients.urls'), name='client'),
    path('redirect/', views.redirect_user_based_on_group, name='redirect_user_based_on_group' )
]
