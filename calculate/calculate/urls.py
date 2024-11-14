
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView
from login import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls'), name='login'),
    path('panel/', include('panel.urls'), name='admin'),
    path('clients/', include('clients.urls'), name='client'),
    path('equipment/', include('equipment.urls'), name='equipment'),
    path('suppliers/', include('suppliers.urls'), name='suppliers'),
    path('redirect/', views.redirect_user_based_on_group, name='redirect_user_based_on_group' ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("__reload__/", include("django_browser_reload.urls")),
]
