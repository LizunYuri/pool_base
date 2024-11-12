from django.http import JsonResponse
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .models import ClientModel
from .forms import ClientModelForm, AddClientModelForm



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



# def full_rights(user):




@user_passes_test(is_admin, login_url='access_denied')
def get_clients(request):
    clients = ClientModel.objects.all().order_by('-id')
    client_data_json = [
            {
                'id' : client.id,
                'name' : client.name,
                'city' : client.city,
                'phone' : client.phone,
                'email' : client.email,
                'note' : client.note,
                'manager' : client.responsible.last_name if client.responsible else None,
                } for client in clients
        ]
    return JsonResponse({'clients' : client_data_json})


@user_passes_test(is_admin, login_url='access_denied')
def clients_list(request):
    return render(request, 'components/includes/clients/clients_list.html')



def client_detail(request, client_id):
    client = get_object_or_404(ClientModel, id=client_id)
    return render(request, 'components/includes/clients/client_detail.html', {'client' : client})




@user_passes_test(is_admin, login_url='access_denied')
def delete_client(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(ClientModel, id=client_id)
        client.delete()
        return JsonResponse({'status': 'success', 'message' : 'record delete'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)




@user_passes_test(is_admin, login_url='access_denied')
def client_edit(request, client_id):
    client = get_object_or_404(ClientModel, id=client_id)

    if request.method == 'POST':
        form = ClientModelForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
    else:
        form = ClientModelForm(instance=client)

    return render(request, 'components/includes/clients/client_update.html', {'form': form, 'client': client})


@user_passes_test(is_admin, login_url='access_denied')
def create_client(request):
    form = None  # Инициализация переменной 'form'

    if request.method == 'POST':
        form = AddClientModelForm(request.POST, current_user=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True}) 
        else:
            return JsonResponse({"success": False, "errors": form.errors})  # Возвращаем ошибки, если форма невалидна
    

    else:  
        form = AddClientModelForm(current_user=request.user)

    return render(request, 'components/includes/clients/client_create.html', {'form': form})



@user_passes_test(is_admin, login_url='access_denied')
def search_clients(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            input_data = data.get('input_data', '')

            clients = ClientModel.objects.filter(
                Q(name__icontains=input_data) |
                Q(city__icontains=input_data) |
                Q(phone__icontains=input_data) |
                Q(email__icontains=input_data)
                )
            client_data_search_json = [
                {
                    'id' : client.id,
                    'name' : client.name,
                    'city' : client.city,
                    'phone' : client.phone,
                    'email' : client.email,
                    } for client in clients
            ]
            print(input_data)

            print(client_data_search_json)

            return JsonResponse({'message': f'Вы искали: {input_data}', 'clients' : client_data_search_json})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ошибка в формате данных JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Некорректный метод запроса'}, status=405)

