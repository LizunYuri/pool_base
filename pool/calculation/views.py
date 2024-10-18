from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from catalogs.models import FinishingMaterialsModel, PumpsModel, HeatingModel, SetDesinfectionModelCL, SetDesinfectionModelRX, HydrolysisModel, EntranceModel
from clients.models import ClientModel
from .forms import CalulateRectangleForm, ClientModelForm
from .models import CalulateRectangleModel
import math
from django.db.models import Q


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
                'model' : desinfection.model_name,
            } for desinfection in desinfections
        ]
    elif SetDesinfectionModelRX.objects.filter(type_category=type_desinfection).exists():
        desinfections = SetDesinfectionModelRX.objects.filter(type_category=type_desinfection)
        model_name = 'SetDesinfectionModelRX'  # Название модели
        desinfection_list = [
            {
                'id': desinfection.id,
                'name': desinfection.name,
                'model' : desinfection.model_name,
            } for desinfection in desinfections
        ]
    elif HydrolysisModel.objects.filter(type_category=type_desinfection).exists():
        desinfections = HydrolysisModel.objects.filter(type_category=type_desinfection)
        model_name = 'HydrolysisModel'  # Название модели
        desinfection_list = [
            {
                'id': desinfection.id,
                'name': desinfection.name,
                'model' : desinfection.model_name,
            } for desinfection in desinfections
        ]
    else:
        return JsonResponse({'error': 'No records found for this type'}, status=404)

    response = {
        'desinfections': desinfection_list,
        'model_name': model_name  # Добавляем название модели в ответ
    }

    return JsonResponse(response, safe=False)

def get_entrance(request):
    entrance_type = request.GET.get('entrance_type')
    entrances = EntranceModel.objects.filter(type_category=entrance_type)

    entrances_list = [{
            'id' : entrance.id,
            'name' : entrance.name
        } for entrance in entrances
        ]
    return JsonResponse({'entrances' : entrances_list})


@csrf_exempt
def accept_size(request):
    if request.method == 'POST':

        def safe_float(value):
            try:
                return float(value) if value else 0.0
            except ValueError:
                return 0.0

        # Получаем данные из POST-запроса и преобразуем их в float
        length = safe_float(request.POST.get('length', ''))
        width = safe_float(request.POST.get('width', ''))
        depth_from = safe_float(request.POST.get('depth_from', ''))
        depth_to = safe_float(request.POST.get('depth_to', ''))
        water_exchange_time = safe_float(request.POST.get('water_exchange_time', ''))
        filtration_speed = safe_float(request.POST.get('filtration_speed', ''))


        # Вычисляем среднюю глубину
        average_depth = (depth_from + depth_to) / 2
        
        # Вычисляем объём, мощность насоса и площадь фильтра
        volume = length * width * average_depth
        pump_power = volume / water_exchange_time
        filtrat_area = pump_power / filtration_speed


        # Вычисление площади зеркала воды, колличество скиммеров (взято срежднее значение из расчет аскиммер на 20м2 зеркала воды)и форсунок

        water_surface_area = length * width
        number_of_skimmers = math.ceil(water_surface_area / 20)
        number_of_nozzles = number_of_skimmers * 2
        
        material_area = ((length  * average_depth) *2) + ((width * average_depth) * 2) + water_surface_area
        material_area_final = math.ceil(material_area + (material_area * 0.25))

        response_data = {
            'message': 'Данные обработаны успешно',
            'volume': volume,
            'length' : length,
            'width' : width,
            'depth_from': depth_from,
            'depth_to' : depth_to,
            'water_surface_area' : water_surface_area,
            'number_of_skimmers' : number_of_skimmers,
            'pump_power' : pump_power,
            'filtrat_area' : filtrat_area,
            'material_area_final' : material_area_final
        }

        request.session['pump-data'] = {
                'pump_power' : pump_power,

            }
        
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Неправильный метод запроса'}, status=400)


def get_filtred_pumps(request):
    pump_power = request.session.get('pump-data', {}).get('pump_power', 0.0)

    matching_pumps = PumpsModel.objects.filter(power__gte=pump_power).order_by('power')

    first_matching_pump = matching_pumps.first()

    if first_matching_pump:
        selected_power = first_matching_pump.power

        result_pumps = PumpsModel.objects.filter(
            Q(power=selected_power) | Q(power=selected_power - 1) | Q(power=selected_power + 1)

            )
    else: 
        result_pumps = PumpsModel.objects.none()
    
    return JsonResponse({
        'pumps' : list(result_pumps.values('id', 'power', 'name'))
        })



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
            ligth_quantity = request.POST.get('ligth_quantity', 0)
            client = form.cleaned_data.get('client')
            digging = form.cleaned_data.get('digging')
            export = form.cleaned_data.get('export')
            concrete = request.POST.get('concrete')

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
                heating = None

            desinfection_id = request.POST.get('desinfection')
            pit_value = request.POST.get('pit', 'false')
            pit = pit_value == 'true'
            cover_value = request.POST.get('cover', 'false')
            cover = cover_value == 'true'
            winding_value = request.POST.get('winding', 'false')
            winding = winding_value  == 'true'
            cleaner_value = request.POST.get('cleaner', 'false')
            cleaner = cleaner_value  == 'true'

            

            # Проверяем значения перед расчетами
            if length and width and depth_from and depth_to and water_exchange_time and filtration_speed:
                average = (depth_from + depth_to) / 2
                area = length * width
                volume = area * average
                pump_power = volume / water_exchange_time
                filter_area = pump_power / filtration_speed

                # Отладочный вывод расчетов
                print(f"Area: {area}, Volume: {volume}, Pump power: {pump_power}, Filter area: {filter_area}")
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
                    heating = heating,
                    desinfection = desinfection_id,
                    pit = pit,
                    cover = cover,
                    winding = winding,
                    cleaner = cleaner,
                    digging = digging,
                    export = export,
                    concrete = concrete,

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

