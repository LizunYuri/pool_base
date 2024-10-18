from django.contrib import admin
from django.urls import path, include
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('main.urls')),
    path('update/', include('catalogs.urls')),
    path('calculation/', include('calculation.urls'))
]
