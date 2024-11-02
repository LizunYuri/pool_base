from django.db import models
import os
from django.utils import timezone



class InertMaterialsModel(models.Model):
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='Для отображения в коммерческом предложении',
                            )
    price = models.FloatField(verbose_name='Стоимость за м3',
                                help_text='',
                                blank=True,
                                default=True)

    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)

    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
        
    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Инертные материалы'    


class ConcreteModel(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Будет указано в коммерческом предложении')
    calculation = models.BooleanField(verbose_name='Участвует в расчете',
                                      help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным',
                                      default=True)
    price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за .м3')
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Бетон'
        verbose_name_plural = 'Бетон от завода'


class FootingModel(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Будет указано в коммерческом предложении')
    calculation = models.BooleanField(verbose_name='Участвует в расчете',
                                      help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным',
                                      default=True)
    price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за .м3')
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материал для подбетонки'


class ReinforcementModel(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Будет указано в коммерческом предложении')
    calculation = models.BooleanField(verbose_name='Участвует в расчете',
                                      help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным',
                                      default=True)
    reinforcement_diameter = models.FloatField(verbose_name='Диаметр арматуры',
                                        help_text='в миллиметрах.',
                                       blank=True,
                                       default=0.0)
    price =  models.FloatField(default=0,
                              null=True,
                              blank=True,

                              verbose_name='Розничная стоимость за .м')
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Арматура'
        verbose_name_plural = 'Арматура'    


class ExcavationRequirementsModel(models.Model):
    CHOICE_POOL_CONSTRUCTION = [
            ('poly', 'Полипропиленовый бассейн'),
            ('mosaic', 'Бетонный бассейн с покрытием мозаикой'),
            ('pvh', 'Бетонный бассейн с покрытием пленкой ПВХ'),
            ('composite', 'Композитный бассейн'),
            ('steel', 'Бессейн из нержавеющей стали'),
        ]
    CHOICE_POOL_FILTRATION = [
            ('skimmer', 'Скиммерный бассейн'),
            ('overflow', 'Переливной бассейн'),
        ]
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='Для отображения в коммерческом предложении',
                            )
    construction = models.CharField(max_length=30,
                                    verbose_name='тип бассейна',
                                    choices=CHOICE_POOL_CONSTRUCTION,
                                    default='pvh',
                                    )
    filtration = models.CharField(max_length=30,
                                    verbose_name='Тип фильтрации',
                                    choices=CHOICE_POOL_FILTRATION,
                                    default='skimmer',
                                    )
    wall_thickness = models.FloatField(verbose_name='Толщина стен',
                                       help_text='в миллиметрах для расчета необходимого количества бетона',)
    slab_thickness = models.FloatField(verbose_name='Толщина плиты',
                                       help_text='в миллиметрах для расчета необходимого количества бетона',)
    concrete_materials = models.ForeignKey(ConcreteModel,
                                          verbose_name='Марка бетона',
                                          help_text='Бетон используемый для отливки стен и основания',
                                          on_delete=models.CASCADE,
                                          )
    bedding_thickness = models.FloatField(verbose_name='Толщина подсыпки',
                                       help_text='в миллиметрах для расчета необходимого количества инертных материалов. (не обязательно)',
                                       blank=True,
                                       default=0.0)
    bedding_materials = models.ForeignKey(InertMaterialsModel,
                                          verbose_name='Материал для подсыпки',
                                          help_text='',
                                          on_delete=models.CASCADE,
                                          default='',
                                          blank=True,
                                          null=True,
                                          )
    footing_thickness = models.FloatField(verbose_name='Толщина подбетонки',
                                        help_text='в миллиметрах для расчета необходимого количества материалов. (не обязательно)',
                                        blank=True,
                                        default=0.0)
    footing_materials = models.ForeignKey(FootingModel,
                                          verbose_name='Материал для подбетонки',
                                          help_text='',
                                          on_delete=models.CASCADE,
                                          default=0,
                                          blank=True,
                                          null=True,
                                          )
    reinforcement = models.ForeignKey(ReinforcementModel,
                                        verbose_name='Арматура',
                                        help_text='.',
                                       blank=True,
                                       default=0.0,
                                       on_delete=models.CASCADE)
    cell_size = models.FloatField(verbose_name='Размер ячейки',
                                        help_text='в миллиметрах для расчета необходимого количества материалов.',
                                       blank=True,
                                       default=0.0)
    number_of_rows  = models.IntegerField(verbose_name='Количество рядов ',
                                        help_text='Для расчета необходимого количества материалов.',
                                       blank=True,
                                       default=0.0)
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    
    def save(self, *args, **kwargs):

        self.wall_thickness = round(self.wall_thickness, 2)
        self.bedding_thickness = round(self.bedding_thickness, 2)
        self.slab_thickness = round(self.slab_thickness, 2)
        self.slab_thickness = round(self.slab_thickness, 2)
        self.cell_size = round(self.cell_size, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return f'{self.construction} | {self.filtration} | {self.name}'
        
    class Meta:
        verbose_name = 'Характеристики'
        verbose_name_plural = 'Технические характеристики для бетнирования чаши'
