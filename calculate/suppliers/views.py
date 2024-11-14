from django.http import JsonResponse
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .models import SupplierModel
from equipment.models import PumpsModel


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




def get_suppliers(request):
    suppliers = SupplierModel.objects.all()

    supplier_data_json = [
            {
                'id' : supplier.id,
                'name' : supplier.name,
                'manager' : supplier.manager,
                'phone' : supplier.phone,
                'legal_name' : supplier.legal_name
                
                } for supplier in suppliers
        ]
    return JsonResponse({'suppliers' : supplier_data_json})



@user_passes_test(is_admin, login_url='access_denied')
def suppliers_list(request):
    return render(request, 'components/includes/supplier/suppliers_list.html')



def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(SupplierModel, id=supplier_id)

    pumps = PumpsModel.objects.filter(supplier=supplier)

    supplier_models_name = {
            'pumps' : PumpsModel._meta.verbose_name_plural,
        }


    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     pumps_list_json = [
    #         {
    #             'id': pump.id,
    #             'name': pump.name,
    #             'price': pump.price,
    #             'article': pump.article
    #         } for pump in pumps
    #     ]
    #     return JsonResponse({'pumps': pumps_list_json})

        

    return render(request, 'components/includes/supplier/supplier_detail.html', {'category' : supplier_models_name, 'supplier' : supplier})

