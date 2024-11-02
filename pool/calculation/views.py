import json
from queue import Full
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from catalogs.models import FilterElementModel, LightingSetModel, ValveGroupModel, ZacladModel, FinishingMaterialsModel, FilterModel, PumpsModel, HeatingModel, SetDesinfectionModelCL, SetDesinfectionModelRX, HydrolysisModel, EntranceModel
from clients.models import ClientModel
from construction.models import ExcavationRequirementsModel
from .forms import CalulateRectangleForm, ClientModelForm
from .models import CalulateRectangleModel
import math
from django.db.models import Q
from django.apps import apps


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


        # Вычисление площади зеркала воды, колличество скиммеров (взято среднее значение из расчета скиммер на 20м2 зеркала воды) и форсунок

        water_surface_area = (length) * (width)
        number_of_skimmers = math.ceil(water_surface_area / 20)
        number_of_nozzles = number_of_skimmers * 2
        
        material_area = ((length  * average_depth) *2) + ((width * average_depth) * 2) + ((length + 0.1) * (width + 0.1))
        material_area_final = math.ceil(material_area + (material_area * 0.20))

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
            'material_area_final' : material_area_final,
        }

        request.session['pump-data'] = {
                'pump_power' : pump_power,
                'filtrat_area' : filtrat_area,
                'water_surface_area' : water_surface_area,
                'number_of_skimmers' : number_of_skimmers,
                'pump_power' : pump_power,
                'material_area_final' : material_area_final,
                'volume': volume,
                'number_of_nozzles' : number_of_nozzles,
                'length' : length,
                'width' : width,
                'depth_from': depth_from,
                'depth_to' : depth_to,
            }
        
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Неправильный метод запроса'}, status=400)


@csrf_exempt
def get_accept_filters(request):
    if request.method == 'POST':

        def safe_float(value):
            try:
                return float(value) if value else 0.0
            except ValueError:
                return 0.0

        filters_materials = safe_float(request.POST.get('filters_materials', ''))



        response_data = {
            'filters_materials' : filters_materials
        }

        request.session['filter-valve-data'] = {
                'filters_materials' : filters_materials,
                }

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Неправильный метод запроса'}, status=400)


@csrf_exempt
def get_accept_lighting(request):
    request.session['test_key'] = 'test_value'
    if request.method == 'POST':
        def safe_float(value):
            try:
                return float(value) if value else 0.0
            except ValueError:
                return 0.0
            
        lighting_materials = request.POST.get('lighting_materials')


        request.session['lighting_elements'] = {
                'lighting_materials': lighting_materials,
            }
        request.session.modified = True
        request.session.save()

        print('Сессия после сохранения:', request.session.items())  # Проверяем, что данные сохранены
        response_data = {
            'lighting_materials': lighting_materials
        }

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Неправильный метод запроса'}, status=400)

def get_materials(request):
    material_type = request.GET.get('type')
    materials = FinishingMaterialsModel.objects.filter(type_materials=material_type)
    

    materials_list = [
            {'id': material.id,
            'name': material.name,
            'price' : material.price
            } for material in materials
         ]
    
    request.session['material-data'] = {
                'material_type' : material_type,
            }
    
    return JsonResponse({'materials': materials_list})

# Функция для полученя закладных элементов
def get_zaclad_elements(request, zaclad_type):
    zaclad_material = request.GET.get('zaclad_material')
    elements = ZacladModel.objects.filter(type_zaclad=zaclad_type, type_materials=zaclad_material)
    
    request.session['zaclad-material'] = {
                'zaclad_material' : zaclad_material
            }
    
    elements_list = [
        {
            'id': element.id,
            'name': element.name,
            'price': element.price,
        } for element in elements
    ]
    return JsonResponse({zaclad_type: elements_list})


def get_lighting(request):
    lighting_session_data = request.session.get('lighting_elements', {})
    lighting_materials = lighting_session_data.get('lighting_materials', '')
    zaclad_material_session = request.session.get('zaclad-material', {'zaclad_material': 'abs'})
    zaclad_material = zaclad_material_session.get('zaclad_material', 'abs')

    if lighting_materials == 'none':
        lighting_elements_list = []
        total_sum = 0
    else:
        lighting_elements = LightingSetModel.objects.filter(
            type_lighting=lighting_materials,
            type_materials=zaclad_material
        )

        lighting_elements_list = []
        total_sum = 0
        for lighting_element in lighting_elements:
            base_price = lighting_element.lamp.price + lighting_element.flask.price
            lighting_data = {
                'id': lighting_element.id,
                'name': lighting_element.name,
                'price': base_price
            }
            total_sum += base_price

            additional_materials_data = []
            additional_materials_sum = 0
            for material in lighting_element.additional_materials.all():
                material_data = {
                    'name': material.name,
                    'price': material.price
                }
                additional_materials_data.append(material_data)
                additional_materials_sum += material.price

            total_sum += additional_materials_sum
            lighting_data['additional_materials'] = additional_materials_data
            lighting_elements_list.append(lighting_data)

    return JsonResponse({
        'lightings': lighting_elements_list,
        'lighting_sum': total_sum,
        'zaclad_material': zaclad_material
    })

def get_skimmers(request):
    return get_zaclad_elements(request, 'skimmer')

def get_nozzle(request):
    return get_zaclad_elements(request, 'nozzle')

def get_bottom_drain(request):
    return get_zaclad_elements(request, 'bottom_drain')

def get_adding_water(request):
    return get_zaclad_elements(request, 'adding_water')

def get_vacuum_clean_nozzle(request):
    return get_zaclad_elements(request, 'vacuum_clean_nozzle')

def get_drain_nozzle(request):
    return get_zaclad_elements(request, 'drain_nozzle')

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
        'pumps' : list(result_pumps.values('id', 'power', 'name', 'price'))
        })

def get_filtred_filter(request):
    filtrat_area = request.session.get('pump-data', {}).get('filtrat_area', 0.0)

    upper_bound = filtrat_area * 1.5
    

    matching_filters = FilterModel.objects.filter(
        filter__gte=filtrat_area,  
        filter__lte=upper_bound    
    )


    return JsonResponse({
        'filters' : list(matching_filters.values('id', 'filter', 'name', 'price', 'valve', 'connection_type' ))
        })

def get_filter_valve(request):
    filter_id = request.session.get('filter-valve-data', {}).get('filters_materials', 0)

    try:
        filter_element = FilterModel.objects.get(id=filter_id)
    except FilterModel.DoesNotExist:
        return JsonResponse({'error': 'Filter not found'}, status=404)

    filter_connection_diameter = filter_element.valve
    filter_connection_type = filter_element.connection_type

    # Временные выводы для проверки
    print("Diameter:", filter_connection_diameter)
    print("Connection Type:", filter_connection_type)

    valves = ValveGroupModel.objects.filter(
        connection_diameter=filter_connection_diameter,
        valve=filter_connection_type
    )

    print("Filtered Valves Count:", len(valves))  # Сколько записей найдено

    valves_list = [
        {
            'id': valve.id,
            'name': valve.name,
            'price': valve.price,
            'valve': valve.get_valve_display(),
            'connection_type': valve.get_connection_type_display()
        } for valve in valves
    ]

    return JsonResponse({'valves': valves_list})

def get_heating(request):
    heating_type = request.GET.get('heating_type')
    heatings = HeatingModel.objects.filter(type_category=heating_type)

    heating_list = [
        {
            'id' : heating.id,
            'name' : heating.name,
            'price' : heating.price,
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
            'name' : entrance.name,
            'price' : entrance.price

        } for entrance in entrances
        ]
    return JsonResponse({'entrances' : entrances_list})

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
            client = form.cleaned_data.get('client')

            length = form.cleaned_data['length']
            width = form.cleaned_data['width']
            depth_from = form.cleaned_data['depth_from']
            depth_to = form.cleaned_data['depth_to']
            

            water_exchange_time = form.cleaned_data['water_exchange_time']
            filtration_speed = form.cleaned_data['filtration_speed']

            pumps_materials_id = request.POST.get('pumps_materials')
            pumps_materials = PumpsModel.objects.get(id=pumps_materials_id)
            pump_power = request.session.get('pump-data', {}).get('pump_power', 0.0)

            two_pumps_value  = request.POST.get('two-pumps', 'false')
            two_pumps = two_pumps_value == 'true'
            pumps_quality = 1

            if two_pumps == True:
                pumps_quality = 2
            else:
                pumps_quality = 1

            pumps_price = pumps_materials.price
            pumps_summ = pumps_price * pumps_quality


            filtrat_area = request.session.get('pump-data', {}).get('filtrat_area', 0.0)
            filters_materials_id = request.POST.get('filters_materials')
            filters_materials = FilterModel.objects.get(id=filters_materials_id)
            two_filters_value  = request.POST.get('two-filters', 'false')
            two_filters = two_filters_value == 'true'
            filters_materials_element_qyantity = filters_materials.sand

            filters_quality = 1

            if two_filters == True:
                filters_quality = 2
            else:
                filters_quality = 1

            filters_price = filters_materials.price
            filters_summ = filters_price * filters_quality

            valve_id = request.POST.get('valve_group')

            valve = ValveGroupModel.objects.get(id=valve_id)
            valve_price = valve.price
            valve_amount = filters_quality
            valve_summ = valve_price * valve_amount

            
            # Получаем объект filter_element напрямую
            filter_element = form.cleaned_data['filter_element']

            # Если это объект модели, используем его свойства
            if isinstance(filter_element, FilterElementModel):
                filter_element_price = filter_element.price
                filter_element_quantity_per_unit = filter_element.quantity_per_unit
                filter_element_quantity = math.ceil((filters_materials_element_qyantity * filters_quality) / filter_element_quantity_per_unit)
                filter_element_summ = filter_element_price * filter_element_quantity
            else:
                raise ValueError("Ожидался объект модели FilterElementModel, но получено что-то другое.")


            material_id = request.POST.get('finished_materials')
            material = FinishingMaterialsModel.objects.get(id=material_id)
            material_price = material.price
            material_area_final = request.session.get('pump-data', {}).get('material_area_final', 0.0)
            material_summ = material_price * material_area_final

            if material.works:
                material_work_name = material.works.name
                material_work_price = material.works.price
                material_work_summ = material_area_final * material_work_price 
            else:
                material_work_name = None
                material_work_price = None
                material_work_summ = None

            if material.type_materials == 'pvh':
                additional_materials = material.additional_materials.all()

                corner_name = ''
                corner_price = 0
                corner_summ = 0
                corner_unit_of_measurement = ''
                textile_name = ''
                textile_price = 0
                textile_summ = 0
                textile_unit_of_measurement = ''
                glue_name = ''
                glue_price = 0
                glue_summ = 0
                glue_unit_of_measurement = ''
                pvc_glue_name = ''
                pvc_glue_price = 0
                pvc_glue_summ = 0
                pvc_glue_unit_of_measurement = ''


                for additional_material in additional_materials:
                    additional_material_info = {
                        'name': additional_material.name,
                        'price': additional_material.price,
                        'unit_of_measurement': additional_material.unit_of_measurement,
                        'type_material': additional_material.type_material
                    }

                    if additional_material_info['type_material'] == 'corner':
                        corner_name = additional_material_info['name']
                        corner_unit_of_measurement = additional_material_info['unit_of_measurement']
                        corner_price = additional_material_info['price']
                        corner_quantity = (length + width) * 2
                        corner_summ = corner_quantity * corner_price
                    elif additional_material_info['type_material'] == 'textile':
                        textile_name = additional_material_info['name']
                        textile_unit_of_measurement = additional_material_info['unit_of_measurement']
                        textile_price = additional_material_info['price']
                        textile_quantity = material_area_final
                        textile_summ = textile_quantity * textile_price
                    elif additional_material_info['type_material'] == 'glue':
                        glue_name = additional_material_info['name']
                        glue_unit_of_measurement = additional_material_info['unit_of_measurement']
                        glue_price = additional_material_info['price']
                        glue_quantity = material_area_final / 7
                        glue_summ = glue_quantity * glue_price
                    elif additional_material_info['type_material'] == 'pvc_glue':
                        pvc_glue_name = additional_material_info['name']
                        pvc_glue_unit_of_measurement = additional_material_info['unit_of_measurement']
                        pvc_glue_price = additional_material_info['price']
                        pvc_glue_quantity = material_area_final / 100
                        pvc_glue_summ = pvc_glue_quantity * pvc_glue_price
            else:
                # Если тип материала не 'pvh'
                corner_name = ''
                corner_price = 0
                corner_summ = 0
                corner_quantity = 0
                corner_unit_of_measurement = ''
                textile_name = ''
                textile_price = 0
                textile_summ = 0
                textile_quantity = 0
                textile_unit_of_measurement = ''
                glue_name = ''
                glue_price = 0
                glue_summ = 0
                glue_quantity = 0
                glue_unit_of_measurement = ''
                pvc_glue_name = ''
                pvc_glue_price = 0
                pvc_glue_summ = 0
                pvc_glue_unit_of_measurement = ''
                pvc_glue_quantity = 0
            
            zaclad_material = request.POST.get('zaclad_material')

            skimmers_id = request.POST.get('skimmers-value')
            skimmers = ZacladModel.objects.get(id = skimmers_id)
            number_of_skimmers = request.session.get('pump-data', {}).get('number_of_skimmers', 0)
            skimmers_price = skimmers.price
            skimmers_summ = skimmers_price * number_of_skimmers

            nozzle_id = request.POST.get('nozzles-value')
            nozzle = ZacladModel.objects.get(id = nozzle_id)
            number_of_nozzles = request.session.get('pump-data', {}).get('number_of_nozzles', 0)
            nozzle_price = nozzle.price
            nozzle_summ = nozzle_price * number_of_nozzles

            bottom_drain_id = request.POST.get('bottom_drain-value')
            if bottom_drain_id:
                try:
                    bottom_drain = ZacladModel.objects.get(id=bottom_drain_id)
                    bottom_drain_amount = 1
                    bottom_drain_price = bottom_drain.price
                    bottom_drain_summ = bottom_drain_price * bottom_drain_amount
                except ZacladModel.DoesNotExist:
                    bottom_drain = ''
                    bottom_drain_amount = 0
                    bottom_drain_price = 0
                    bottom_drain_summ = 0
            else:
                bottom_drain = ''
                bottom_drain_amount = 0
                bottom_drain_price = 0
                bottom_drain_summ = 0

            adding_water_id = request.POST.get('adding_water-value')
            if adding_water_id:
                try:
                    adding_water = ZacladModel.objects.get(id=adding_water_id)
                    adding_water_amount = 1
                    adding_water_price = adding_water.price
                    adding_water_summ = adding_water_price * adding_water_amount
                except ZacladModel.DoesNotExist:
                    adding_water = ''
                    adding_water_amount = 0
                    adding_water_price = 0
                    adding_water_summ = 0
            else:
                adding_water = ''
                adding_water_amount = 0
                adding_water_price = 0
                adding_water_summ = 0

            drain_nozzle_id = request.POST.get('drain_nozzle-value')
            if drain_nozzle_id:
                try:
                    drain_nozzle = ZacladModel.objects.get(id=drain_nozzle_id)
                    drain_nozzle_amount = 1
                    drain_nozzle_price = drain_nozzle.price
                    drain_nozzle_summ = drain_nozzle_price * drain_nozzle_amount
                except ZacladModel.DoesNotExist:
                    drain_nozzle = ''
                    drain_nozzle_amount = 0
                    drain_nozzle_price = 0
                    drain_nozzle_summ = 0
            else:
                drain_nozzle = ''
                drain_nozzle_amount = 0
                drain_nozzle_price = 0
                drain_nozzle_summ = 0

            vacuum_clean_nozzle_id = request.POST.get('vacuum_clean_nozzle-value')
            if vacuum_clean_nozzle_id:
                try:
                    vacuum_clean_nozzle = ZacladModel.objects.get(id=vacuum_clean_nozzle_id)
                    vacuum_clean_nozzle_amount = 1
                    vacuum_clean_nozzle_price = vacuum_clean_nozzle.price
                    vacuum_clean_nozzle_summ = vacuum_clean_nozzle_price * vacuum_clean_nozzle_amount
                except ZacladModel.DoesNotExist:
                    vacuum_clean_nozzle = ''
                    vacuum_clean_nozzle_amount = 0
                    vacuum_clean_nozzle_price = 0
                    vacuum_clean_nozzle_summ = 0
            else:
                vacuum_clean_nozzle = ''
                vacuum_clean_nozzle_amount = 0
                vacuum_clean_nozzle_price = 0
                vacuum_clean_nozzle_summ = 0



            ligthing_data = request.POST.get('lighting_dropdown')
            if ligthing_data:
                ligthing_id = int(ligthing_data)
            else:
                ligthing_id = 0
                lighting_json_data = {}


            ligthing = request.POST.get('lighting')
            ligth_quantity = request.POST.get('ligth_quantity', 0)

            if ligthing == 'none':
                ligth_quantity = 0
                ligthing_id = 0
                lighting_json_data = {}
            else:
                if ligthing_id > 0:
                    ligthing_summ = 0
                    ligthing_element = LightingSetModel.objects.get(id=ligthing_id)

                    
                    ligthing_summ = ligthing_element.lamp.price + ligthing_element.flask.price

                    lighting_json_data = {
                        'name': ligthing_element.name,
                        'set': {
                            'lamp_name': ligthing_element.lamp.name,
                            'lamp_price': ligthing_element.lamp.price,
                            'flask_name': ligthing_element.flask.name,
                            'flask_price': ligthing_element.flask.price,
                        }
                    }
                    
                    additional_materials_data = []
                    additional_materials_sum = 0

                    for material in ligthing_element.additional_materials.all():
                        material_data = {
                            'name': material.name,
                            'price': material.price
                        }
                        additional_materials_data.append(material_data)
                        additional_materials_sum += material.price

                    
                    ligthing_summ += additional_materials_sum

                    lighting_json_data['adittional_elements'] = additional_materials_data
                    
                    lighting_json_data['ligthing_summ'] = ligthing_summ


            heating_id = request.POST.get('heating')

            if heating_id:  # Проверяем, есть ли значение в heating_id
                try:
                    heating = HeatingModel.objects.get(id=heating_id)
                    print(heating.additional_equipment.all())
                    heating_json_data = {
                            'name' : heating.name,
                            'price' : heating.price,
                        }
                    adittionals_heating_data = []
                    adittioonals_heating_summ = 0

                    for material in heating.additional_equipment.all():
                        adittional_heating_data = {
                                'name' : material.name,
                                'price' : material.price
                            }
                        adittionals_heating_data.append(adittional_heating_data)
                        adittioonals_heating_summ += material.price

                    heating_summ = heating.price + adittioonals_heating_summ

                    heating_json_data.update({
                            'adittionals_heating' : adittionals_heating_data,
                            'heating_summ' : heating_summ
                        })

                except HeatingModel.DoesNotExist:
                    heating_json_data = {}
                    heating = None
            else:
                heating_json_data = {}
                heating = None

            desinfection_data = request.POST.get('desinfection')

            if desinfection_data:
                desinfection_parts = desinfection_data.split('|')

                if len(desinfection_parts) == 2:
                    desinfection_id, desinfection_model_name = desinfection_parts
                    desinfection_id = int(desinfection_id)

                    
                    DesinfectionModel = apps.get_model('catalogs', desinfection_model_name)
                    
                    desinfection_data_json = {}

                    if desinfection_model_name == 'SetDesinfectionModelRX':
                        DesinfectionModel = apps.get_model('catalogs', desinfection_model_name)
                        desinfection_instance = DesinfectionModel.objects.get(id=desinfection_id)
                        desinfection_instance_name = desinfection_instance.name
                        desinfection_data_json ={
                            'name' : desinfection_instance.name,
                            'rx_name' : desinfection_instance.rx_name,
                            'rx_price' : desinfection_instance.rx_price,
                            'ph_name' : desinfection_instance.ph_name,
                            'ph_price' : desinfection_instance.ph_price,
                            'rx_liquid_name' : desinfection_instance.rx_liquid_name,
                            'rx_liquid_price' : desinfection_instance.rx_liquid_price,
                            'ph_liquid_name' : desinfection_instance.ph_liquid_name,
                            'ph_liquid_price' : desinfection_instance.ph_liquid_price,
                            'desinfrction_summ' : desinfection_instance.rx_price + desinfection_instance.ph_price + desinfection_instance.rx_liquid_price + desinfection_instance.ph_liquid_price
                            }
                    elif desinfection_model_name == 'SetDesinfectionModelCL':
                        DesinfectionModel = apps.get_model('catalogs', desinfection_model_name)
                        desinfection_instance = DesinfectionModel.objects.get(id=desinfection_id)
                        desinfection_instance_name = desinfection_instance.name
                        desinfection_data_json ={
                            'name' : desinfection_instance.name,
                            'price' : desinfection_instance.price,
                            'rx_liquid_name' : desinfection_instance.rx_liquid_name,
                            'rx_liquid_price' : desinfection_instance.rx_liquid_price,
                            'ph_liquid_name' : desinfection_instance.ph_liquid_name,
                            'ph_liquid_price' : desinfection_instance.ph_liquid_price,
                            'desinfrction_summ' : desinfection_instance.price + desinfection_instance.rx_liquid_price + desinfection_instance.ph_liquid_price
                            }
                    elif desinfection_model_name == 'HydrolysisModel':
                        DesinfectionModel = apps.get_model('catalogs', desinfection_model_name)
                        desinfection_instance = DesinfectionModel.objects.get(id=desinfection_id)
                        desinfection_instance_name = desinfection_instance.name
                        desinfection_data_json ={
                            'name' : desinfection_instance.name,
                            'price' : desinfection_instance.price,
                            'ph_liquid_name' : desinfection_instance.ph_liquid_name,
                            'ph_liquid_price' : desinfection_instance.ph_liquid_price,
                            'desinfrction_summ' : desinfection_instance.price + desinfection_instance.ph_liquid_price
                            }
                    if desinfection_data_json:  # Если переменная не пустая
                        desinfection_json = json.dumps(desinfection_data_json)
                    else:
                        desinfection_json = json.dumps({}) 

                else:
                    
                    desinfection_id = desinfection_parts[0] if desinfection_parts[0] else None
                    desinfection_instance_name = ''
                    desinfection_data_json = {} 
                    desinfection_json = {}
            else:
                # Обрабатываем случай, если ничего не выбрано
                desinfection_instance_name = ''
                desinfection_data_json = {}
                desinfection_json = {}

            ultraviolet =  form.cleaned_data['ultraviolet']

            pit_value = request.POST.get('pit', 'false')
            pit = pit_value == 'true'

            cover_value = request.POST.get('cover', 'false')
            cover = cover_value == 'true'

            winding_value = request.POST.get('winding', 'false')
            winding = winding_value  == 'true'

            cleaner_value = request.POST.get('cleaner', 'false')
            cleaner = cleaner_value  == 'true'

            
            entrance_materials_id = request.POST.get('entrance_materials')
            entrance_materials = EntranceModel.objects.get(id=entrance_materials_id)

            
            water_surface_area = request.session.get('pump-data', {}).get('water_surface_area', 0.0)
            
            
            
            volume = request.session.get('pump-data', {}).get('volume', 0.0)


            

            digging = form.cleaned_data.get('digging')
            
            export = form.cleaned_data.get('export')


            concrete = request.POST.get('concrete')

            size_session_data = request.session.get('pub-data', {})


            material_session_data = request.session.get('material-data', {})

            material_session_length = length
            material_session_width = width
            material_session_depth_from = depth_from
            material_session_depth_to = depth_to
            material_session_depth = (material_session_depth_from + material_session_depth_to) / 2

            concrete_data_json = {}

            if concrete == '1':
                material_data_type = material_session_data.get('material_type' , '')
                if material_data_type == 'pvh':
                    excavation_data = ExcavationRequirementsModel.objects.filter(
                        construction=material_data_type
                    ).order_by('-date').first()

                    wall_thinckeness = excavation_data.wall_thickness / 1000
                    slab_thinckeness = excavation_data.slab_thickness / 1000
                    concrete_materials = excavation_data.concrete_materials
                    concrete_materials_price = excavation_data.concrete_materials.price
                    number_of_rows = excavation_data.number_of_rows
                    reinforcement = excavation_data.reinforcement
                    reinforcement_price = excavation_data.reinforcement.price

                    bedding_thickness = excavation_data.bedding_thickness / 1000

                    footing_thickness = excavation_data.footing_thickness / 1000

                    # получение финального размера стен и площади основания
                    final_lenght = material_session_length + (wall_thinckeness * 2 )
                    final_width = material_session_width  + (wall_thinckeness * 2 )
                    final_volume = (final_lenght * final_width)

                    # расчет бетона 

                    volume_concrete = final_volume * slab_thinckeness
                    long_wall_concrete = round((final_lenght * material_session_depth * slab_thinckeness) * 2, 2)
                    short_wall_concrete = round((final_width * material_session_depth * slab_thinckeness) * 2, 2)
                    total_wall_concrete = long_wall_concrete + short_wall_concrete

                    volume_concrete_summ = volume_concrete * concrete_materials_price
                    total_wall_concrete_summ = total_wall_concrete * concrete_materials_price

                    # расчет арматуры

                    length_reinforcement = round((2 + (final_lenght / slab_thinckeness) * number_of_rows), 0)
                    width_reinforcement = round((2 + (final_width / slab_thinckeness) * number_of_rows), 0)
                    total_cell_plate = (length_reinforcement * final_lenght) + (width_reinforcement * final_width)

                    long_wall_reinforcement_lenght = round((2 + (final_lenght / wall_thinckeness) * number_of_rows), 0)
                    long_wall_reinforcement_depth = round((2 + (material_session_depth / wall_thinckeness) * number_of_rows), 0)
                    total_long_wall_reinforcement = (long_wall_reinforcement_depth + long_wall_reinforcement_lenght) * 2
                    

                    short_wall_reinforcement_width = round((2 + (final_width / wall_thinckeness) * number_of_rows), 0)
                    short_wall_reinforcement_depth = round((2 + (material_session_depth / wall_thinckeness) * number_of_rows), 0)
                    total_short_wall_reinforcement = (short_wall_reinforcement_width + short_wall_reinforcement_depth) * 2
                    total_wall_reinforcement = total_long_wall_reinforcement + total_short_wall_reinforcement


                    if bedding_thickness !=0:
                        bedding_thickness_volume = round(final_volume * bedding_thickness, 0)
                        bedding_thickness_materials = excavation_data.bedding_materials.name
                        bedding_thickness_summ = excavation_data.bedding_materials.price * bedding_thickness_volume
                    else:
                        bedding_thickness_volume = 0
                        bedding_thickness_materials = ''
                        bedding_thickness_summ = 0


                    if footing_thickness !=0:
                        footing_thickness_volume = round(final_volume * footing_thickness, 0)
                        footing_thickness_materials = excavation_data.footing_materials.name
                        footing_thickness_summ = excavation_data.footing_materials.price * footing_thickness_volume
                    else:
                        footing_thickness_volume = 0
                        footing_thickness_materials = ''
                        footing_thickness_summ = 0


                    concrete_data_json = {
                            'concrete_materials' : concrete_materials.name,
                            'concrete_materials_price' : concrete_materials_price,
                            'volume_concrete' : volume_concrete,
                            'volume_concrete_summ' : volume_concrete_summ,
                            'total_wall_concrete' : total_wall_concrete,
                            'total_wall_concrete_summ' : total_wall_concrete_summ,
                            
                            'reinforcement' : reinforcement.name,
                            'reinforcement_price' : reinforcement_price,
                            'total_cell_plate' : total_cell_plate,
                            'cell_reinforcement_summ' : total_cell_plate * reinforcement_price,
                            'total_wall_reinforcement' : total_wall_reinforcement,
                            'wall_reinforcement_summ' : total_wall_reinforcement * reinforcement_price,
                            
                            'bedding_thickness_volume' : bedding_thickness_volume,
                            'bedding_thickness_materials' : bedding_thickness_materials,
                            'bedding_thickness_summ' : bedding_thickness_summ,

                            'footing_thickness_volume' : footing_thickness_volume,
                            'footing_thickness_materials' : footing_thickness_materials,
                            'footing_thickness_summ' : footing_thickness_summ,

                            'total_summ' : float((volume_concrete_summ + total_wall_concrete_summ + (total_cell_plate * reinforcement_price) + (total_wall_reinforcement * reinforcement_price) + bedding_thickness_summ + footing_thickness_summ), 0)
                        }
                    print(material_session_length, material_session_width, final_lenght, final_width, final_volume, concrete_data_json)
                else:
                    concrete_data_json = {}


            
            if length and width and depth_from and depth_to and water_exchange_time and filtration_speed:


                
                rectangle = CalulateRectangleModel(
                    client = client, 
                    length = length,
                    width = width,
                    depth_from = depth_from,
                    depth_to = depth_to,
                    water_exchange_time = water_exchange_time,
                    filtration_speed = filtration_speed,
                    pump_power = pump_power,
                    pump_name = pumps_materials,
                    two_pumps = two_pumps,
                    pumps_quality = pumps_quality,
                    pumps_price = pumps_price,
                    pumps_summ = pumps_summ,
                    filter_area = filtrat_area,
                    filter_name = filters_materials,
                    two_filters = two_filters,
                    valve_name = valve,
                    valve_price = valve_price,
                    valve_amount = valve_amount,
                    valve_summ = valve_summ,
                    filters_quality = filters_quality,
                    filters_price = filters_price,
                    filters_summ = filters_summ,
                    filter_element = filter_element,
                    filter_element_price = filter_element_price,
                    filter_element_quantity = filter_element_quantity,
                    filter_element_summ = filter_element_summ,
                    finished_materials = material.name,
                    finished_manetrals_area = material_area_final,
                    finished_material_price = material_price,
                    finished_material_summ = material_summ,
                    finished_material_work_name = material_work_name,
                    finished_material_work_price = material_work_price,
                    finished_material_work_summ =material_work_summ,
                    finished_manetral_work_qyality = material_area_final,
                    finished_material_corner_name = corner_name,
                    finished_material_corner_price = corner_price,
                    finished_manetral_corner_qyality = corner_quantity,
                    finished_material_corner_summ = corner_summ,
                    finished_material_corner_unit_of_measurement = corner_unit_of_measurement,
                    finished_material_textile_name = textile_name,
                    finished_manetral_textile_qyality =textile_quantity,
                    finished_material_textile_price = textile_price,
                    finished_material_textile_summ = textile_summ,
                    finished_material_textile_unit_of_measurement = textile_unit_of_measurement,
                    finished_material_glue_name = glue_name,
                    finished_manetral_glue_qyality =glue_quantity,
                    finished_material_glue_price = glue_price,
                    finished_material_glue_summ = glue_summ,
                    finished_material_glue_unit_of_measurement = glue_unit_of_measurement,
                    finished_material_pvc_glue_name = pvc_glue_name,
                    finished_material_pvc_glue_qyality = pvc_glue_quantity,
                    finished_material_pvc_glue_price = pvc_glue_price,
                    finished_material_pvc_glue_summ = pvc_glue_summ,
                    finished_material_pvc_glue_unit_of_measurement = pvc_glue_unit_of_measurement,
                    zaclad_material = zaclad_material,
                    skimmers_name = skimmers,
                    skimmers_price = skimmers_price,
                    skimmers_amount = number_of_skimmers,
                    skimmers_summ = skimmers_summ,
                    nozzle_name = nozzle,
                    nozzle_price = nozzle_price,
                    nozzle_amount = number_of_nozzles,
                    nozzle_summ = nozzle_summ,
                    bottom_drain_name = bottom_drain,
                    bottom_drain_price = bottom_drain_price,
                    bottom_drain_amount = bottom_drain_amount,
                    bottom_drain_summ = bottom_drain_summ,
                    adding_water_name = adding_water,
                    adding_water_price = adding_water_price,
                    adding_water_amount = adding_water_amount,
                    adding_water_summ = adding_water_summ,
                    drain_nozzle_name = drain_nozzle,
                    drain_nozzle_price = drain_nozzle_price,
                    drain_nozzle_amount = drain_nozzle_amount,
                    drain_nozzle_summ = drain_nozzle_summ,
                    vacuum_clean_nozzle_name = vacuum_clean_nozzle,
                    vacuum_clean_nozzle_price = vacuum_clean_nozzle_price,
                    vacuum_clean_nozzle_amount = vacuum_clean_nozzle_amount,
                    vacuum_clean_nozzle_summ = vacuum_clean_nozzle_summ,
                    desinfection = desinfection_json,
                    ligthing = lighting_json_data,
                    ligth_quantity = ligth_quantity,
                    heating = heating_json_data,
                    ultraviolet = ultraviolet,
                    pit = pit,
                    cover = cover,
                    winding = winding,
                    cleaner = cleaner,
                    concrete = concrete_data_json,
                    export = export,
                    digging = digging,
                    entrance = entrance_materials,
                    number_of_skimmers = number_of_skimmers,
                    number_of_nozzles = number_of_nozzles,
                    volume=volume,
                    area=water_surface_area,
                )
                rectangle.save()
                return redirect('rectangle_detail', pk=rectangle.pk)

        else:
            print(form.errors)  
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

