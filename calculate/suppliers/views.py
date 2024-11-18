from email import message
from django.contrib import messages
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
from .forms import CreateSupplierModelForm


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

    # Передаем и имя модели, и сам QuerySet
    supplier_data = {
        'pumps': {
            'verbose_name': PumpsModel._meta.verbose_name_plural,
            'items': pumps
        }
    }

    return render(request, 'components/includes/supplier/supplier_detail.html', {
        'category': supplier_data,
        'supplier': supplier
    })


@user_passes_test(is_admin, login_url='access_denied')
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(SupplierModel, id=supplier_id)

    # проверка наличия связанных записей
    related_record = {
            'pumps' : PumpsModel.objects.filter(supplier=supplier).exists(),
        }
    
    if any(related_record.values()):
        messages.error(request, 'Удалить запись невозможно! Так как есть связанные товары.')
        return JsonResponse ({'error': 'Удалить запись невозможно! Так как есть связанные товары.'})
    
    supplier.delete()
    messages.success(request, 'Запись удалена')
    return JsonResponse({'success' : 'Запись удалена'})


@user_passes_test(is_admin, login_url='access_denied')
def create_supplier(request):
    form = None

    if request.method == 'POST':
        form = CreateSupplierModelForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success" : True})
        else:
            return JsonResponse({'success': False, 'errors' : form.errors})
    else:
        # Инициализируем пустую форму для GET-запроса
        form = CreateSupplierModelForm()    

    return render(request, 'components/includes/supplier/supplier_create.html', {'form': form})


@user_passes_test(is_admin, login_url='access_denied')
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(SupplierModel, id=supplier_id)

    form = None
    if request.method == 'POST':
        form = CreateSupplierModelForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
        else:
            form = CreateSupplierModelForm(instance=supplier)

    return render(request, 'components/includes/supplier/supplier_update.html', {'form': form, 'supplier': supplier} )


@user_passes_test(is_admin, login_url='access_denied')
def search_supplier(request):
    if request.method == 'POST':
        try: 
            data = json.loads(request.body)
            input_data = data.get('input_data', '')
            suppliers = SupplierModel.objects.filter(
                Q(name__icontains=input_data) |
                Q(legal_name__icontains=input_data) |
                Q(manager__icontains=input_data) |
                Q(phone__icontains=input_data) |
                Q(email__icontains=input_data) 
                )
            supplier_data_json = [
                {
                    'id' : supplier.id,
                    'name' : supplier.name,
                    'manager' : supplier.manager,
                    'phone' : supplier.phone,
                    'legal_name' : supplier.legal_name
                    
                } for supplier in suppliers
            ]
            return JsonResponse({'message': f'Вы искали: {input_data}', 'suppliers' : supplier_data_json})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ошибка в формате данных JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Некорректный метод запроса'}, status=405)

            