from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.http import JsonResponse
from clients.models import ClientModel


def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Администратор").exists()


@user_passes_test(is_admin, login_url='access_denied')
def panel_admin(request):
    
    return render(request, "panel/admin_panel.html")


def access_denied(request):
    return render(request, "errors/403.html")
