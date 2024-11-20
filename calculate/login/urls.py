from django.urls import include, path
from . import views



urlpatterns = [
    path('', views.custom_login_view, name='sing_up'),
    path('profile', views.user_profile, name='profile'),
    path('update-profile/', views.update_form, name='update-profile'),
    path('update-profile-save/', views.profile_update, name='update-profile-save'),
    path('403/', views.access_denied, name='access_denied'),
]
