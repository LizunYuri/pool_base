from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .models import ClientModel

def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Администратор").exists()

@user_passes_test(is_admin, login_url='access_denied')
def get_clients(request):
    clients = ClientModel.objects.all()
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
    return render(request, 'components/includes/clients_list.html')

def client_detail(request, client_id):
    client = get_object_or_404(ClientModel, id=client_id)
    return render(request, 'components/includes/client_detail.html', {'client' : client})