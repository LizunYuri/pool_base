# views.py
from django.shortcuts import render, redirect
from .forms import CalulateRectangleForm
from .models import CalulateRectangleModel

def create_rectangle(request):
    if request.method == 'POST':
        form = CalulateRectangleForm(request.POST)
        if form.is_valid():
            length = form.cleaned_data['length']
            width = form.cleaned_data['width']
            depth_from = form.cleaned_data['depth_from']
            depth_to = form.cleaned_data['depth_to']
            water_exchange_time = form.cleaned_data['water_exchange_time']
            filtration_speed = form.cleaned_data['filtration_speed']
            
            # Отладочный вывод
            print(f"Length: {length}, Width: {width}, Depth from: {depth_from}, Depth to: {depth_to}, Water exchange time: {water_exchange_time}, Filtration speed: {filtration_speed}")

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
                    client=form.cleaned_data['client'],
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
                )
                rectangle.save()
                return redirect('rectangle_detail', pk=rectangle.pk)
        else:
            print(form.errors)  # Выводим ошибки формы для отладки
    else:
        form = CalulateRectangleForm()

    return render(request, 'calculation/create_rectangle.html', {'form': form})



def rectangle_detail(request, pk):
    rectangle = CalulateRectangleModel.objects.get(pk=pk)
    return render(request, 'calculation/rectangle_detail.html', {'rectangle': rectangle})
