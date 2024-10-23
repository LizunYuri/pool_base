from django.db import models
from clients.models import ClientModel
from catalogs.models import ExportModel, DiggingModel, FilterElementModel
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
    
    water_exchange_time = models.FloatField(max_length=20,
                                            choices=CHOICES_WATER_TIME,
                                            default=4,
                                            verbose_name='Время полного водообмена',
                                            help_text='Для частного бассейна необходимо 6 часов, для бассейнов в небольших гостиницах 4 часа',
                                        )
    filtration_speed= models.FloatField(max_length=20,
                                        choices=CHOICES_WATER_FILTRATION_SPEED,
                                        default=20,
                                        verbose_name='Скорость фильтрации',
                                        help_text='Чем ниже скорость тем качественнее очистка воды',
                                        )
    pump_power = models.FloatField(verbose_name='Рекомендованная мощность насоса', 
                                    null=True,
                                    blank=True,
                                    editable=False
                                    )
    pump_name = models.CharField(max_length=300,
                                verbose_name='Наименование насоса',
                                help_text='Заполняется автоматически',
                                blank=True,
                                editable=False)
    two_pumps = models.BooleanField(verbose_name='Резервный насос',
                                    help_text='Увеличивает количество насосов вдвое',
                                    default=False,
                                    editable=False
                                    )
    pumps_quality = models.IntegerField(verbose_name='Количество насосов',
                                        default=0,
                                        blank=True,
                                        editable=False,
                                        help_text='Заполняется автоматически'
                                        )
    pumps_price = models.FloatField(verbose_name='Цена насоса',
                                    help_text='Заполняется из базы',
                                    blank=True,
                                    default=0,
                                    editable=False
                                    )
    pumps_summ = models.FloatField(verbose_name='Сумма за насосы',
                                    help_text='',
                                    blank=True,
                                    default=0,
                                    editable=False
                                    )
    filter_area = models.FloatField(verbose_name='Рекомендованная площадь фильтра', 
                                    null=True,
                                    blank=True,
                                    editable=False
                                    )
    filter_name = models.CharField(max_length=300,
                                    verbose_name='Наименование фильтра',
                                    help_text='Заполняется автоматически',
                                    blank=True,
                                    editable=False
                                    )
    two_filters = models.BooleanField(verbose_name='Замедление фильтрации',
                                    help_text='Количество фильтров увеличивается вдвое',
                                    default=False
                                    )
    filters_quality = models.IntegerField(verbose_name='Количество фильтров',
                                        default=0,
                                        blank=True,
                                        editable=False,
                                        help_text='Заполняется автоматически'
                                        )
    filters_price = models.FloatField(verbose_name='Цена фильтра',
                                    help_text='Заполняется из базы',
                                    blank=True,
                                    default=0,
                                    editable=False
                                    )
    filters_summ = models.FloatField(verbose_name='Сумма за фильтры',
                                    help_text='',
                                    blank=True,
                                    default=0,
                                    editable=False
                                    )
    filter_element = models.ForeignKey(FilterElementModel,
                               verbose_name='Фильтрующий элемент',
                               help_text='Выбрать из имеющегося',
                               on_delete=models.CASCADE,
                               null=True, 
                               blank=True,
                               )
    filter_element_price = models.FloatField(verbose_name='Цена за единицу фильтрующего эелмента',
                                    help_text='Заполняется из базы',
                                    blank=True,
                                    default=0,
                                    editable=False
                                    )
    filter_element_quantity = models.FloatField(verbose_name='Количество мешков',
                                    help_text='Заполняется из базы',
                                    blank=True,
                                    default=0,
                                    editable=False
                                    )
    filter_element_summ = models.FloatField(verbose_name='Сумма за песок',
                                    help_text='Заполняется из базы',
                                    blank=True,
                                    default=0,
                                    editable=False
                                    )

    finished_materials = models.CharField(max_length=200,
                                          verbose_name='Материал',
                                          help_text='Финишная отделка',
                                          editable=False
                                          )
    finished_manetrals_area = models.FloatField(verbose_name='Количество материалов',
                                                help_text='',
                                                blank=True,
                                                editable=False
                                                )
    finished_material_price = models.FloatField(verbose_name='Стоимость за м2',
                                                help_text='',
                                                blank=True,
                                                editable=False
                                                )
    finished_material_summ = models.FloatField(verbose_name='Сумма за материал',
                                                help_text='',
                                                blank=True,
                                                editable=False
                                                )
    finished_material_work_name = models.CharField(max_length=200,
                                          verbose_name='Работы по пленке отделке',
                                          help_text='Финишная отделка',
                                          editable=False
                                          )
    finished_material_work_price = models.FloatField(verbose_name='Стоимость работ',
                                                help_text='',
                                                blank=True,
                                                editable=False
                                                )
    finished_material_work_summ = models.FloatField(verbose_name='Сумма за работы',
                                                help_text='',
                                                blank=True,
                                                editable=False
                                                )
    finished_manetral_work_qyality= models.FloatField(verbose_name='Количество материалов',
                                                help_text='',
                                                blank=True,
                                                editable=False,
                                                default=0
                                                )
    finished_material_corner_name = models.CharField(max_length=200,
                                          verbose_name='Угол с напылением ПВХ',
                                          help_text='Финишная отделка',
                                          editable=False,
                                          blank=True,
                                          default=''
                                          )
    finished_manetral_corner_qyality= models.FloatField(verbose_name='Количество материалов',
                                                help_text='',
                                                blank=True,
                                                editable=False,
                                                default=0
                                                )
    finished_material_corner_price = models.FloatField(verbose_name='Цена уголка с напылением ПВХ',
                                                help_text='',
                                                blank=True,
                                                default=0,
                                                null=True,
                                                editable=False
                                                )
    finished_material_corner_summ = models.FloatField(verbose_name='Сумма за Угол с напылением ПВХ',
                                                help_text='',
                                                blank=True,
                                                default=0,
                                                null=True,
                                                editable=False
                                                )
    finished_material_corner_unit_of_measurement = models.CharField(max_length=200,
                                          verbose_name='единица измерения',
                                          help_text='Финишная отделка',
                                          editable=False,
                                          blank=True,
                                          default=''
                                          )
    finished_material_textile_name = models.CharField(max_length=200,
                                          verbose_name='Гео текстиль',
                                          help_text='Финишная отделка',
                                          editable=False,
                                          blank=True,
                                          default=''
                                          )
    finished_material_textile_price = models.FloatField(verbose_name='цена за единицу',
                                                help_text='',
                                                blank=True,
                                                default=0,
                                                null=True,
                                                editable=False
                                                )
    finished_manetral_textile_qyality= models.FloatField(verbose_name='Количество материалов',
                                                help_text='',
                                                blank=True,
                                                editable=False,
                                                default=0
                                                )
    finished_material_textile_summ = models.FloatField(verbose_name='сумма за геотекстиль',
                                                help_text='',
                                                blank=True,
                                                default=0,
                                                null=True,
                                                editable=False
                                                )
    finished_material_textile_unit_of_measurement = models.CharField(max_length=200,
                                          verbose_name='единица измерения',
                                          help_text='Финишная отделка',
                                          editable=False,
                                          blank=True,
                                          default=''
                                          )
    finished_material_glue_name = models.CharField(max_length=200,
                                          verbose_name='Клей геотекстиля',
                                          help_text='Финишная отделка',
                                          editable=False,
                                          blank=True,
                                          default=''
                                          )
    finished_material_glue_price = models.FloatField(verbose_name='Стоимость',
                                                help_text='',
                                                blank=True,
                                                default=0,
                                                null=True,
                                                editable=False
                                                )
    finished_manetral_glue_qyality= models.FloatField(verbose_name='Количество материалов',
                                                help_text='',
                                                blank=True,
                                                editable=False,
                                                default=0
                                                )
    finished_material_glue_summ = models.FloatField(verbose_name='Сумма за клей',
                                                help_text='',
                                                blank=True,
                                                default=0,
                                                null=True,
                                                editable=False
                                                )
    finished_material_glue_unit_of_measurement = models.CharField(max_length=200,
                                          verbose_name='Жидкий ПВХ',
                                          help_text='Финишная отделка',
                                          editable=False,
                                          blank=True,
                                          default=''
                                          )
    finished_material_pvc_glue_qyality = models.FloatField(verbose_name='Стоимость',
                                                help_text='',
                                                blank=True,
                                                default=0,
                                                null=True,
                                                editable=False
                                                )
    finished_material_pvc_glue_name = models.CharField(max_length=200,
                                          verbose_name='Работы по пленке отделке',
                                          help_text='Финишная отделка',
                                          editable=False,
                                          blank=True,
                                          default=''
                                          )
    finished_material_pvc_glue_price = models.FloatField(verbose_name='Стоимость работ',
                                                help_text='',
                                                blank=True,
                                                default=0,
                                                null=True,
                                                editable=False
                                                )
    finished_material_pvc_glue_summ = models.FloatField(verbose_name='Сумма за работы',
                                                help_text='',
                                                blank=True,
                                                default=0,
                                                null=True,
                                                editable=False
                                                )
    finished_material_pvc_glue_unit_of_measurement = models.CharField(max_length=200,
                                          verbose_name='Работы по пленке отделке',
                                          help_text='Финишная отделка',
                                          editable=False,
                                          blank=True,
                                          default=''
                                          )
    zaclad_material = models.CharField(max_length=200,
                                        verbose_name='Материал закладнных',
                                        help_text='Финишная отделка',
                                        blank=True, 
                                        editable=False
                                        )
    ligthing = models.CharField(max_length=200,
                                verbose_name='Освещение',
                                help_text='Подводное освещение',
                                blank=True, 
                                editable=False
                                )
    ligth_quantity = models.IntegerField(verbose_name='Количество ламп',
                                        help_text='Количество ламп',
                                        blank=True, 
                                        null=True,
                                        editable=False
                                        )        
    heating = models.CharField(max_length=200,
                                verbose_name='Подогрев',
                                help_text='Подогрев воды в бассейне',
                                blank=True,
                                null=True, 
                                editable=False
                                )
    desinfection = models.CharField(max_length=200,
                                    verbose_name='Дезинфекция',
                                    help_text='Дозирующее оборудование',
                                    blank=True, 
                                    editable=False
                                    )   
    pit  = models.BooleanField(default=False,
                               verbose_name='Приямок',
                                help_text='Полипропиленовый приямок',
                                blank=True, 
                                editable=False
                                )
    cover  = models.BooleanField(default=False,
                               verbose_name='Покрывало',
                                help_text='Плавающее покрывало',
                                blank=True, 
                                editable=False
                                ) 
    winding  = models.BooleanField(default=False,
                               verbose_name='Сматывающее устройство',
                                help_text='Сматывающее устройство',
                                blank=True, 
                                editable=False
                                )
    cleaner  = models.BooleanField(default=False,
                               verbose_name='Пылесос',
                                help_text='Подводный пылесос',
                                blank=True, 
                                editable=False
                                )
    concrete = models.IntegerField(verbose_name='Бетонные работы',
                                   editable=False,
                                   blank=True,
                                   null=True,
                                   default=0
                                   )
    digging = models.ForeignKey(DiggingModel,
                                verbose_name='Разработка котлована',
                                help_text='Выбрать из имеющегося',
                                on_delete=models.CASCADE
                                )
    export = models.ForeignKey(ExportModel,
                               verbose_name='Вывоз грунта',
                               help_text='Выбрать из имеющегося',
                               on_delete=models.CASCADE
                               )
    entrance = models.CharField(max_length=200,
                                verbose_name='Входная группа',
                                help_text='Заполняется из выбранного пользователем',
                                editable=False,
                                blank=True
                                )
    number_of_skimmers = models.IntegerField(verbose_name='',
                                            help_text='',
                                            editable=False,
                                            )
    number_of_nozzles = models.IntegerField(verbose_name='',
                                            help_text='',
                                            default=0,
                                            editable=False,
                                            blank=True
                                            )
    volume = models.FloatField(verbose_name='Объем бассейна', 
                               null=True, blank=True, editable=False)
    area = models.FloatField(verbose_name='Площадь зеркала воды', 
                               null=True, blank=True, editable=False)


    def save(self, *args, **kwargs):

        self.length = round(self.length, 2)
        self.width = round(self.width, 2)
        self.depth_from = round(self.depth_from, 2)
        self.depth_to = round(self.depth_to, 2)
        self.finished_material_price = round(self.finished_material_price , 2)
        self.finished_material_summ = round(self.finished_material_summ , 2)


        super().save(*args, **kwargs)

    def __str__(self): 
        return self.client.name
    
    class Meta:
        verbose_name = 'Расчет'
        verbose_name_plural = 'Расчет скиммерного прямоугольного бассейна'    
# # circle