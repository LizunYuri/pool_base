from django.shortcuts import render, redirect
from django.http import JsonResponse
from catalogs.models import FinishingMaterialsModel, HeatingModel, SetDesinfectionModelCL, SetDesinfectionModelRX, HydrolysisModel 
from clients.models import ClientModel
from .forms import CalulateRectangleForm, ClientModelForm
from .models import CalulateRectangleModel

def get_materials(request):
    material_type = request.GET.get('type')
    materials = FinishingMaterialsModel.objects.filter(type_materials=material_type)
    

    materials_list = [{'id': material.id, 'name': material.name} for material in materials]
    
    return JsonResponse({'materials': materials_list})

def get_heating(request):
    heating_type = request.GET.get('heating_type')
    heatings = HeatingModel.objects.filter(type_category=heating_type)

    heating_list = [
        {
            'id' : heating.id,
            'name' : heating.name
            } for heating in heatings
        ]
    return JsonResponse({'heatings' : heating_list})

def get_desinfection(request):
    type_desinfection = request.GET.get('type_desinfection')

    desinfection_list = []
    model_name = None

    if SetDesinfectionModelCL.objects.filter(type_category=type_desinfection).exists():
        desinfections = SetDesinfectionModelCL.objects.filter(type_category=type_desinfection)
        model_name = 'SetDesinfectionModelCL'  # Название модели
        desinfection_list = [
            {
                'id': desinfection.id,
                'name': desinfection.name,
            } for desinfection in desinfections
        ]
    elif SetDesinfectionModelRX.objects.filter(type_category=type_desinfection).exists():
        desinfections = SetDesinfectionModelRX.objects.filter(type_category=type_desinfection)
        model_name = 'SetDesinfectionModelRX'  # Название модели
        desinfection_list = [
            {
                'id': desinfection.id,
                'name': desinfection.name,
            } for desinfection in desinfections
        ]
    elif HydrolysisModel.objects.filter(type_category=type_desinfection).exists():
        desinfections = HydrolysisModel.objects.filter(type_category=type_desinfection)
        model_name = 'HydrolysisModel'  # Название модели
        desinfection_list = [
            {
                'id': desinfection.id,
                'name': desinfection.name,
            } for desinfection in desinfections
        ]
    else:
        return JsonResponse({'error': 'No records found for this type'}, status=404)

    response = {
        'desinfections': desinfection_list,
        'model_name': model_name  # Добавляем название модели в ответ
    }

    return JsonResponse(response, safe=False)
 

def create_client(request):
    if request.method == 'POST':
        form = ClientModelForm(request.POST)
        if form.is_valid():
            client = form.save()
            # Возвращаем данные нового клиента в формате JSON
            return JsonResponse({
                'success': True,
                'client': {
                    'id': client.id,
                    'name': client.name,
                }
            })
        else:
            # Если форма не валидна, отправляем ошибки
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    else:
        return JsonResponse({'success': False, 'error': 'Неправильный метод запроса'})

def create_rectangle(request):
    step = request.POST.get('step', '1')

    if request.method == 'POST':
        form = CalulateRectangleForm(request.POST)
        client_form = ClientModelForm(request.POST)

        if step == '1':
            if 'create_client' in request.POST:
                if client_form.is_valid():
                    new_client = client_form.save()
                if request.is_ajax():
                    return JsonResponse({
                        'client_id': new_client.id,
                        'client_name': str(new_client)
                    })
                form = CalulateRectangleForm(initial={
                    'form': form,
                    'client_form': client_form,
                    'new_client_add': True
                })

        # Если основная форма отправлена
        if form.is_valid():
            length = form.cleaned_data['length']
            width = form.cleaned_data['width']
            depth_from = form.cleaned_data['depth_from']
            depth_to = form.cleaned_data['depth_to']
            water_exchange_time = form.cleaned_data['water_exchange_time']
            filtration_speed = form.cleaned_data['filtration_speed']
            zaclad_material = request.POST.get('zaclad_material')
            ligthing = request.POST.get('ligthing')
            ligth_quantity = request.POST.get('ligth_quantity')
            # Получение клиента (если клиент может быть необязательным)
            client = form.cleaned_data.get('client')

            # Получение материала
            material_id = request.POST.get('finished_materials')
            material = FinishingMaterialsModel.objects.get(id=material_id)

            heating_id = request.POST.get('heating')

            if heating_id:  # Проверяем, есть ли значение в heating_id
                try:
                    heating = HeatingModel.objects.get(id=heating_id)
                except HeatingModel.DoesNotExist:

                    heating = None
            else:
                heating = None  # Если значение пустое, устанавливаем heating в None

            desinfection_id = request.POST.get('desinfection')
            model_name = request.POST.get('model_name')

            print("Desinfection ID:", desinfection_id)
            print("Model Name:", model_name) 

            # Проверяем значения перед расчетами
            if length and width and depth_from and depth_to and water_exchange_time and filtration_speed:
                average = (depth_from + depth_to) / 2
                area = length * width
                volume = area * average
                pump_power = volume / water_exchange_time
                filter_area = pump_power / filtration_speed

                # Отладочный вывод расчетов
                print(f"Area: {area}, Volume: {volume}, Pump power: {pump_power}, Filter area: {filter_area}")
                print(model_name)
                rectangle = CalulateRectangleModel(
                    client=client, 
                    length=length,
                    width=width,
                    depth_from=depth_from,
                    depth_to=depth_to,
                    water_exchange_time=water_exchange_time,
                    filtration_speed=filtration_speed,
                    volume=volume,
                    area=area,
                    pump_power=pump_power,
                    filter_area=filter_area,
                    finished_materials=material.name,
                    zaclad_material = zaclad_material,
                    ligthing = ligthing,
                    ligth_quantity = ligth_quantity,
                    heating = heating
                )
                rectangle.save()
                return redirect('rectangle_detail', pk=rectangle.pk)

        else:
            print(form.errors)  # Выводим ошибки формы для отладки
    else:
        form = CalulateRectangleForm()
        client_form = ClientModelForm()

    return render(request, 'calculation/create_rectangle.html', {
        'form': form,
        'client_form': client_form
    })

def rectangle_detail(request, pk):
    rectangle = CalulateRectangleModel.objects.get(pk=pk)
    return render(request, 'calculation/rectangle_detail.html', {'rectangle': rectangle})

