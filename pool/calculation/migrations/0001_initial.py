# Generated by Django 3.2 on 2024-10-23 07:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogs', '0001_initial'),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalulateRectangleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата расчета', null=True, verbose_name='Дата')),
                ('length', models.FloatField(help_text='По внутрянке', verbose_name='Длинна бассейна')),
                ('width', models.FloatField(help_text='по внутрянке', verbose_name='Ширина бассейна')),
                ('depth_from', models.FloatField(help_text='Перепад глубины не больше 10см на 1 метр', verbose_name='Глубина от')),
                ('depth_to', models.FloatField(help_text='В случае прямого дна поствить то же что и в Глубина от', verbose_name='Глубина до')),
                ('water_exchange_time', models.FloatField(choices=[(6.0, '6 часов'), (4.0, '4 часа'), (2.0, '2 часа'), (1.0, '1 час'), (0.5, '30 минут')], default=4, help_text='Для частного бассейна необходимо 6 часов, для бассейнов в небольших гостиницах 4 часа', max_length=20, verbose_name='Время полного водообмена')),
                ('filtration_speed', models.FloatField(choices=[(30, '30 м/ч'), (20, '20 м/ч'), (10, '10 м/ч')], default=20, help_text='Чем ниже скорость тем качественнее очистка воды', max_length=20, verbose_name='Скорость фильтрации')),
                ('pump_power', models.FloatField(blank=True, editable=False, null=True, verbose_name='Рекомендованная мощность насоса')),
                ('pump_name', models.CharField(blank=True, editable=False, help_text='Заполняется автоматически', max_length=300, verbose_name='Наименование насоса')),
                ('two_pumps', models.BooleanField(default=False, editable=False, help_text='Увеличивает количество насосов вдвое', verbose_name='Резервный насос')),
                ('filter_area', models.FloatField(blank=True, editable=False, null=True, verbose_name='Рекомендованная площадь фильтра')),
                ('filter_name', models.CharField(blank=True, editable=False, help_text='Заполняется автоматически', max_length=300, verbose_name='Наименование фильтра')),
                ('two_filters', models.BooleanField(default=False, help_text='Количество фильтров увеличивается вдвое', verbose_name='Замедление фильтрации')),
                ('finished_materials', models.CharField(editable=False, help_text='Финишная отделка', max_length=200, verbose_name='Материал')),
                ('finished_manetrals_area', models.FloatField(blank=True, editable=False, verbose_name='Количество материалов')),
                ('finished_material_price', models.FloatField(blank=True, editable=False, verbose_name='Стоимость за м2')),
                ('finished_material_summ', models.FloatField(blank=True, editable=False, verbose_name='Сумма за материал')),
                ('zaclad_material', models.CharField(blank=True, editable=False, help_text='Финишная отделка', max_length=200, verbose_name='Материал закладнных')),
                ('ligthing', models.CharField(blank=True, editable=False, help_text='Подводное освещение', max_length=200, verbose_name='Освещение')),
                ('ligth_quantity', models.IntegerField(blank=True, editable=False, help_text='Количество ламп', null=True, verbose_name='Количество ламп')),
                ('heating', models.CharField(blank=True, editable=False, help_text='Подогрев воды в бассейне', max_length=200, null=True, verbose_name='Подогрев')),
                ('desinfection', models.CharField(blank=True, editable=False, help_text='Дозирующее оборудование', max_length=200, verbose_name='Дезинфекция')),
                ('pit', models.BooleanField(blank=True, default=False, editable=False, help_text='Полипропиленовый приямок', verbose_name='Приямок')),
                ('cover', models.BooleanField(blank=True, default=False, editable=False, help_text='Плавающее покрывало', verbose_name='Покрывало')),
                ('winding', models.BooleanField(blank=True, default=False, editable=False, help_text='Сматывающее устройство', verbose_name='Сматывающее устройство')),
                ('cleaner', models.BooleanField(blank=True, default=False, editable=False, help_text='Подводный пылесос', verbose_name='Пылесос')),
                ('concrete', models.IntegerField(blank=True, default=0, editable=False, null=True, verbose_name='Бетонные работы')),
                ('entrance', models.CharField(blank=True, editable=False, help_text='Заполняется из выбранного пользователем', max_length=200, verbose_name='Входная группа')),
                ('number_of_skimmers', models.IntegerField(editable=False, verbose_name='')),
                ('number_of_nozzles', models.IntegerField(blank=True, default=0, editable=False, verbose_name='')),
                ('volume', models.FloatField(blank=True, editable=False, null=True, verbose_name='Объем бассейна')),
                ('area', models.FloatField(blank=True, editable=False, null=True, verbose_name='Площадь зеркала воды')),
                ('client', models.ForeignKey(help_text='Обязательно к заполнению', on_delete=django.db.models.deletion.CASCADE, to='clients.clientmodel', verbose_name='Клиент')),
                ('digging', models.ForeignKey(help_text='Выбрать из имеющегося', on_delete=django.db.models.deletion.CASCADE, to='catalogs.diggingmodel', verbose_name='Разработка котлована')),
                ('export', models.ForeignKey(help_text='Выбрать из имеющегося', on_delete=django.db.models.deletion.CASCADE, to='catalogs.exportmodel', verbose_name='Вывоз грунта')),
            ],
            options={
                'verbose_name': 'Расчет',
                'verbose_name_plural': 'Расчет скиммерного прямоугольного бассейна',
            },
        ),
    ]
