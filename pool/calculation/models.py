from django.db import models
from clients.models import ClientModel
from catalogs.models import ExportModel, DiggingModel
from django.utils import timezone



class CalulateRectangleModel(models.Model):
    CHOICES_WATER_TIME = [
            (6.0, '6 часов'),
            (4.0, '4 часа'),
            (2.0, '2 часа'),
            (1.0, '1 час'),
            (0.5, '30 минут'),
        ]
    CHOICES_WATER_FILTRATION_SPEED = [
            (30, '30 м/ч'),
            (20, '20 м/ч'),
            (10, '10 м/ч'),
        ]
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата расчета',
                            null=True,
                            blank=True,
                            editable=False)
    client = models.ForeignKey(ClientModel, 
                               verbose_name='Клиент',
                               help_text='Обязательно к заполнению',
                               on_delete=models.CASCADE,)
    length = models.FloatField(verbose_name='Длинна бассейна',
                               help_text='По внутрянке',
                               )
    width = models.FloatField(verbose_name='Ширина бассейна',
                               help_text='по внутрянке',
                               )
    depth_from = models.FloatField(verbose_name='Глубина от',
                               help_text='Перепад глубины не больше 10см на 1 метр',
                               )
    depth_to = models.FloatField(verbose_name='Глубина до',
                               help_text='В случае прямого дна поствить то же что и в Глубина от',
                               )
    water_exchange_time = models.FloatField(
                            max_length=20,
                            choices=CHOICES_WATER_TIME,
                            default=4,
                            verbose_name='Время полного водообмена',
                            help_text='Для частного бассейна необходимо 6 часов, для бассейнов в небольших гостиницах 4 часа',
                            )
    filtration_speed= models.FloatField(
                            max_length=20,
                            choices=CHOICES_WATER_FILTRATION_SPEED,
                            default=20,
                            verbose_name='Скорость фильтрации',
                            help_text='Чем ниже скорость тем качественнее очистка воды',
                            )
    volume = models.FloatField(verbose_name='Объем бассейна', 
                               null=True, blank=True, editable=False)
    area = models.FloatField(verbose_name='Площадь зеркала воды', 
                               null=True, blank=True, editable=False)
    pump_power = models.FloatField(verbose_name='Рекомендованная мощность насоса', 
                               null=True, blank=True, editable=False)
    filter_area = models.FloatField(verbose_name='Рекомендованная площадь фильтра', 
                               null=True, blank=True, editable=False)
    finished_materials = models.CharField(max_length=200,
                                          verbose_name='Материал',
                                          help_text='Финишная отделка',
                                          editable=False)
    zaclad_material = models.CharField(max_length=200,
                                          verbose_name='Материал закладнных',
                                          help_text='Финишная отделка',
                                          blank=True, 
                                          editable=False)
    heating = models.CharField(max_length=200,
                                          verbose_name='Подогрев',
                                          help_text='Подогрев воды в бассейне',
                                          blank=True,
                                          null=True, 
                                          editable=False)
    ligthing = models.CharField(max_length=200,
                                          verbose_name='Освещение',
                                          help_text='Подводное освещение',
                                          blank=True, 
                                          editable=False)
    ligth_quantity = models.IntegerField(verbose_name='Количество ламп',
                                          help_text='Количество ламп',
                                          blank=True, 
                                          null=True,
                                          editable=False)
    desinfection = models.CharField(max_length=200,
                                          verbose_name='Дезинфекция',
                                          help_text='Дозирующее оборудование',
                                          blank=True, 
                                          editable=False)
    pit  = models.BooleanField(default=False,
                               verbose_name='Приямок',
                                help_text='Полипропиленовый приямок',
                                blank=True, 
                                editable=False)
    cover  = models.BooleanField(default=False,
                               verbose_name='Покрывало',
                                help_text='Плавающее покрывало',
                                blank=True, 
                                editable=False)
    winding  = models.BooleanField(default=False,
                               verbose_name='Сматывающее устройство',
                                help_text='Сматывающее устройство',
                                blank=True, 
                                editable=False)
    cleaner  = models.BooleanField(default=False,
                               verbose_name='Пылесос',
                                help_text='Подводный пылесос',
                                blank=True, 
                                editable=False)
    digging = models.ForeignKey(DiggingModel,
                                verbose_name='Разработка котлована',
                                help_text='Выбрать из имеющегося',
                                on_delete=models.CASCADE)
    export = models.ForeignKey(ExportModel,
                               verbose_name='Вывоз грунта',
                               help_text='Выбрать из имеющегося',
                               on_delete=models.CASCADE)
    concrete = models.IntegerField(verbose_name='Бетонные работы',
                                   editable=False,
                                   default=1)
    entrance = models.CharField(max_length=200,
                                verbose_name='Входная группа',
                                help_text='Заполняется из выбранного пользователем',
                                editable=False,
                                blank=True)

    def save(self, *args, **kwargs):

        self.length = round(self.length, 2)
        self.width = round(self.width, 2)
        self.depth_from = round(self.depth_from, 2)
        self.depth_to = round(self.depth_to, 2)


        super().save(*args, **kwargs)

    def __str__(self): 
        return self.client.name
    
    class Meta:
        verbose_name = 'Расчет'
        verbose_name_plural = 'Расчет скиммерного прямоугольного бассейна'    
# # circle