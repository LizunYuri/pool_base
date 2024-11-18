from django.http import JsonResponse
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from equipment.utils import get_records_by_supplier
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


def supplier_records_view(request, supplier_id):
    model_names = [
        'equipment.PumpsModel',
    ]
    records = get_records_by_supplier(supplier_id, model_names)

    # Форматируем результат для JSON-ответа
    response_data = {}
    for model_name, result in records.items():
        if isinstance(result, str):  # Ошибки обработки модели
            response_data[model_name] = result
        elif result.exists():  # Успешная фильтрация
            response_data[model_name] = list(result.values())
        else:  # Нет записей
            response_data[model_name] = "No records found."
    
    return JsonResponse({'records': response_data})
