from queue import Full
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from catalogs.models import FilterElementModel, ZacladModel, FinishingMaterialsModel, FilterModel, PumpsModel, HeatingModel, SetDesinfectionModelCL, SetDesinfectionModelRX, HydrolysisModel, EntranceModel
from clients.models import ClientModel
from .forms import CalulateRectangleForm, ClientModelForm
from .models import CalulateRectangleModel
import math
from django.db.models import Q
from django.apps import apps


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

def get_skimmers(request):
    zaclad_material = request.POST.get('zaclad_material')
    skimmers = ZacladModel.objects.filter(type_zaclad = 'skimmer', type_materials = zaclad_material)
    
    skimmers_list = [
        {
            'id' : skimmer.id,
            'name' : skimmer.name
            } for skimmer in skimmers
        ]
    return JsonResponse({'scimmers' : skimmers_list})


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
            'material_area_final' : material_area_final
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
        'filters' : list(matching_filters.values('id', 'filter', 'name', 'price'))
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
            # material_factor = 0

            # if zaclad_material == 'abs':
            #     material_factor = 1
            # else:
            #     material_factor = 2

            number_of_skimmers = request.session.get('pump-data', {}).get('number_of_skimmers', 0)

            # skimmers = ZacladModel.objects.filter(type_zaclad='scimmer')


            




            ligthing = request.POST.get('ligthing')
            ligth_quantity = request.POST.get('ligth_quantity', 0)

            heating_id = request.POST.get('heating')

            if heating_id:  # Проверяем, есть ли значение в heating_id
                try:
                    heating = HeatingModel.objects.get(id=heating_id)
                except HeatingModel.DoesNotExist:

                    heating = None
            else:
                heating = None

            desinfection_data = request.POST.get('desinfection')

            if desinfection_data:
                desinfection_parts = desinfection_data.split('|')

                if len(desinfection_parts) == 2:
                    desinfection_id, desinfection_model_name = desinfection_parts
                    desinfection_id = int(desinfection_id)

                    
                    DesinfectionModel = apps.get_model('catalogs', desinfection_model_name)
                    desinfection_instance = DesinfectionModel.objects.get(id=desinfection_id)
                    desinfection_instance_name = desinfection_instance.name
                else:
                    # Обрабатываем случай, если значение одно (например, когда ничего не выбрано)
                    desinfection_id = desinfection_parts[0] if desinfection_parts[0] else None
                    desinfection_instance_name = ''  # Или любая другая логика
            else:
                # Обрабатываем случай, если ничего не выбрано
                desinfection_instance_name = ''



            pit_value = request.POST.get('pit', 'false')
            pit = pit_value == 'true'

            cover_value = request.POST.get('cover', 'false')
            cover = cover_value == 'true'

            winding_value = request.POST.get('winding', 'false')
            winding = winding_value  == 'true'

            cleaner_value = request.POST.get('cleaner', 'false')
            cleaner = cleaner_value  == 'true'

            concrete = request.POST.get('concrete')

            digging = form.cleaned_data.get('digging')
            
            export = form.cleaned_data.get('export')
            
            entrance_materials_id = request.POST.get('entrance_materials')
            entrance_materials = EntranceModel.objects.get(id=entrance_materials_id)

            
            
            water_surface_area = request.session.get('pump-data', {}).get('water_surface_area', 0.0)
            
            number_of_nozzles = request.session.get('pump-data', {}).get('number_of_nozzles', 0)
            
            volume = request.session.get('pump-data', {}).get('volume', 0.0)




            


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
                    ligthing = ligthing,
                    ligth_quantity = ligth_quantity,
                    heating = heating,
                    desinfection = desinfection_instance_name,
                    pit = pit,
                    cover = cover,
                    winding = winding,
                    cleaner = cleaner,
                    concrete = concrete,
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

