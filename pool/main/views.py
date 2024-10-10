from django.http import JsonResponse
import json
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from supplier.models import SupplierModel
from catalogs.models import FilterModel, PumpsModel


def panel(request):
    return render(request, 'pages/panel.html')

def accountant_panel(request):
    return render(request, 'pages/accountant_panel.html')

log_messages = []

def export_data(request, model):
    instances = model.objects.all()

    data = [
        {
            'id': instance.pk,
            'name': instance.name,
            'price': instance.price,
            'date': instance.date,
            'status': instance.status,
            "supplier": {
                "id": instance.supplier.pk if instance.supplier else None,
                "name": instance.supplier.name if instance.supplier else None,
                "url": instance.supplier.url if instance.supplier and instance.supplier.url else None,
            },
            "url": instance.product_url if instance.product_url else None,
        }
        for instance in instances
    ]
    
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def update_item(item, model_class):
    """Обновляет элемент модели и возвращает статус обновления."""
    item_id = item.get('id')
    price = item.get('price')
    product_url = item.get('product_url')

    try:
        instance = model_class.objects.get(id=item_id)

        updated = False
        if instance.price != price:
            instance.price = price
            instance.date = timezone.now()
            instance.product_url = product_url if instance.product_url is None else instance.product_url
            instance.save()
            updated = True
            return {'id': item_id, 'status': 'updated'}

        if instance.product_url is None and product_url is not None:
            instance.product_url = product_url
            instance.save()
            updated = True
            return {'id': item_id, 'status': 'url_updated'}

        return {'id': item_id, 'status': 'on_change'}
        
    except model_class.DoesNotExist:
        return {'id': item_id, 'status': 'no_found'}

def export_filters(request):
    return export_data(request, FilterModel)

def export_pumps(request):
    return export_data(request, PumpsModel)

@csrf_exempt
def update_filters(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        updated_filters = [update_item(item, FilterModel) for item in data]
        return JsonResponse(updated_filters, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def update_pumps(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        updated_pumps = [update_item(item, PumpsModel) for item in data]
        return JsonResponse(updated_pumps, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def message_logistic(request):
    
    if request.method == 'POST':
        
        log_message = json.loads(request.body.decode('utf-8'))
        log_messages.append(log_message)
        return JsonResponse({'status': 'success'})
    
    return render(request, 'message/log_message.html', {
        'log_messages': log_messages
    })