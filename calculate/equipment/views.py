from django.http import JsonResponse
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .models import PumpsModel


def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Администратор").exists()

def is_supervisor(user):
    return user.is_authenticated and user.groups.filter(name="Руководитель").exists()

def is_engineer(user):
    return user.is_authenticated and user.groups.filter(name="Инженер").exists()

def is_manager(user):
    return user.is_authenticated and user.groups.filter(name="Менеджер").exists()

def is_accountant(user):
    return user.is_authenticated and user.groups.filter(name="Бухгалтер").exists()




def get_equipment(request):
    pumps = PumpsModel.objects.all()

    pump_data_json = [
            {
                'id' : pump.id,
                'article' : pump.article,
                'name' : pump.name,
                'power' : pump.power,
                'price' : pump.price
                } for pump in pumps
        ]
    return JsonResponse({'pumps' : pump_data_json})



# @user_passes_test(is_admin, login_url='access_denied')
def pumps_list(request):
    return render(request, 'components/includes/equipment/pumps_list.html')