from django.shortcuts import render, redirect
from django.http import JsonResponse
from catalogs.models import FinishingMaterialsModel
from .forms import CalulateRectangleForm, ClientModelForm
from .models import CalulateRectangleModel

def get_materials(request):
    material_type = request.GET.get('type')
    materials = FinishingMaterialsModel.objects.filter(type_materials=material_type)
    
    # Формируем список материалов для отправки
    materials_list = [{'id': material.id, 'name': material.name} for material in materials]
    
    return JsonResponse({'materials': materials_list})

def create_rectangle(request):

    if request.method == 'POST':

        form = CalulateRectangleForm(request.POST)
        client_form = ClientModelForm(request.POST)

        # Если форма создания нового клиента отправлена
        if 'create_client' in request.POST:
            if client_form.is_valid():
                new_client = client_form.save()

                # Обновляем форму с клиентом
                form = CalulateRectangleForm(initial={
                    'client': new_client  # Передаем нового клиента в форму
                })
                
                # Переходим на ту же страницу, чтобы форма обновилась с клиентом
                return render(request, 'calculation/create_rectangle.html', {
                    'form': form,
                    'client_form': client_form,
                    'new_client_added': True  # Можно передать флаг для визуального уведомления
                })

        # Если основная форма отправлена
        if form.is_valid():
            length = form.cleaned_data['length']
            width = form.cleaned_data['width']
            depth_from = form.cleaned_data['depth_from']
            depth_to = form.cleaned_data['depth_to']
            water_exchange_time = form.cleaned_data['water_exchange_time']
            filtration_speed = form.cleaned_data['filtration_speed']
            client = form.cleaned_data['client']
            material_id = request.POST.get('finished_materials')
            material = FinishingMaterialsModel.objects.get(id=material_id)


            # Проверяем значения перед расчетами
            if length and width and depth_from and depth_to and water_exchange_time and filtration_speed:
                # Средняя глубина
                average = (depth_from + depth_to) / 2

                # Площадь зеркала воды
                area = length * width

                # Расчет объема воды
                volume = area * average

                # Расчет мощности насоса
                pump_power = volume / water_exchange_time

                # Расчет площади фильтрации
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

