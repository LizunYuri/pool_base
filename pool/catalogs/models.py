import os
from django.utils import timezone
from django.db import models
from supplier.models import SupplierModel

class AdditionalMaterial(models.Model):
    CHOICE_UNIT_OF_MEASUREMENT = [
        ('psc', 'шт.'),
        ('m_ch', 'м/пог'),
        ('m_2', 'м2'),
        ('kg', 'кг'),
        ]
    CHOICE_TYPE_MATERIAL = [
        ('corner', 'Угол с напылением ПВХ'),
        ('textile', 'Геотекстиль'),
        ('glue', 'Клей для геотекстиля'),
        ('pvc_glue', 'Жидкий ПВХ')
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE,
                                 blank=True,)
    name = models.CharField(max_length=200,
                            verbose_name='Наименование',
                            help_text='Как в каталоге поставщика',)
    unit_of_measurement = models.CharField(
                            max_length=20,
                            choices=CHOICE_UNIT_OF_MEASUREMENT,
                            default='psc',
                            verbose_name='Единица измерения',
                            blank=True,
                            null=True)
    type_material = models.CharField(max_length=20,
                                     choices=CHOICE_TYPE_MATERIAL,
                                     verbose_name='Категория',
                                     help_text='Максимально приближенная')
    price = models.FloatField(default=0, verbose_name="Цена за единицу")
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
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
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Дополнительные материалы для отделки чаши бассейна'
    

class WorkMaterialModel(models.Model):
    CHOICE_UNIT_OF_MEASUREMENT = [
        ('psc', 'шт.'),
        ('m_ch', 'м/пог'),
        ('m_2', 'м2'),
        ('kg', 'кг'),
        ]
    name = models.CharField(max_length=255,
                            verbose_name="Название")
    unit_of_measurement = models.CharField(
                            max_length=20,
                            choices=CHOICE_UNIT_OF_MEASUREMENT,
                            default='psc',
                            verbose_name='Единица измерения',
                            blank=True,
                            null=True)
    price = models.FloatField(default=0, verbose_name="Цена за единицу")

    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Работы по отделке чаши бассейна'


class FilterModel(models.Model):
    TYPE_CONNECTION_CHOICE = [
            ('lateral','Боковое подключение'),
            ('upper','Верхнее подключение'),
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            )
    square = models.IntegerField(verbose_name='Диаметр',
                            help_text='Из каталога поставщика. В мм',
                            default=0.00,
                            blank=True,
                            null=True)
    filter = models.FloatField(verbose_name='Площадь фильтрации',
                            help_text='Из каталога поставщика. в м2',
                            default=0.00,
                            blank=True,
                            null=True)
    sand = models.IntegerField(verbose_name='количество фильтрата',
                            help_text='Из каталога поставщика. В кг',
                            default=0.00,
                            blank=True,
                            null=True)
    valve = models.FloatField(verbose_name='Тип вентиля',
                            default=0.00,
                            blank=True,
                            null=True)
    connection_type = models.CharField(verbose_name='Тип подключения',
                             max_length=20,
                             choices=TYPE_CONNECTION_CHOICE,
                            default='upper',)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    image = models.ImageField(upload_to='catalog/filters/',
                              verbose_name='Фото товара',
                              help_text='Красивое фото используется для коммерческого предложения')
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.square = round(self.square, 2)
        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтровальное оборудование'


class ValveGroupModel(models.Model):
    TYPE_CHOICE = [
            ('automatic', 'Автоматический вентиль'),
            ('manual', 'Ручной вентиль')
        ]
    TYPE_CONNECTION_CHOICE = [
            ('lateral','Боковое подключение'),
            ('upper','Верхнее подключение'),
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 blank=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            blank=True,
                            help_text='В точности как в каталоге поставщика',
                            )
    connection_diameter = models.FloatField(verbose_name='Диаметр подключения',
                            help_text='',
                            default=0.00,
                            null=True)
    connection_type = models.CharField(verbose_name='Тип вентиля',
                             max_length=20,
                             choices=TYPE_CHOICE,
                            default='manual',)
    valve = models.CharField(verbose_name='Тип подключения',
                             max_length=20,
                             choices=TYPE_CONNECTION_CHOICE,
                            default='upper',)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Вентиль'
        verbose_name_plural = 'Вентильная группа'


class FilterElementModel(models.Model):
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200,
                            verbose_name='Наименование',
                            help_text='Номенклатурное наименование')
    quantity_per_unit = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='количество в единице')
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    def save(self, *args, **kwargs):
        
        self.quantity_per_unit = round(self.quantity_per_unit, 2)
        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name

    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Фильтрующий элемент'


class PumpsModel(models.Model):
    CHOICES = [
            ('220v', '220v'),
            ('380v', '380v')
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            )
    power = models.FloatField(verbose_name='Мощность',
                            help_text='Из каталога поставщика. В м3/ч',
                            default=0.00,
                            blank=True,
                            null=True)
    voltage = models.CharField(
                            max_length=20,
                            choices=CHOICES,
                            default='220v',
                            verbose_name='Вольтаж',
                            help_text='220 Вольт / 380вольт',
                            blank=True,
                            null=True)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    image = models.ImageField(upload_to='catalog/pumps/',
                              verbose_name='Фото товара',
                              help_text='Красивое фото используется для коммерческого предложения')
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.power = round(self.power, 2)
        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'Насос'
        verbose_name_plural = 'Насосное оборудование'


class FinishingMaterialsModel(models.Model):
    CHOICES = [
            ('poly', 'Полипропилен'),
            ('pvh', 'Пленка ПВХ')
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    type_materials = models.CharField(
                            max_length=20,
                            choices=CHOICES,
                            default='pvh',
                            verbose_name='Категория материала',
                            help_text='Пленка ПВХ / Полипропилен',
                            blank=True,
                            null=True)
    additional_materials = models.ManyToManyField(
                                        AdditionalMaterial,
                                        blank=True,
                                        verbose_name="Дополнительные материалы",
                                        )
    works = models.ForeignKey(WorkMaterialModel,
                              blank=True,
                              null=True,
                              verbose_name="Работы",
                              on_delete=models.CASCADE)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за м2')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    image = models.ImageField(upload_to='catalog/finished/',
                              verbose_name='Фото товара',
                              help_text='Красивое фото используется для коммерческого предложения')
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Отделочные материалы'


class ZacladModel(models.Model):
    CHOICES = [
            ('abs', 'ABS пластик'),
            ('aisi', 'AISI-316 нержавеющий металл')
        ]
    CHOICES_TYPE = [
            ('skimmer', 'Скиммер'),
            ('nozzle', 'Возвратная фрсунка'),
            ('bottom_drain', 'Донный слив'),
            ('adding_water', 'Долив воды автоматический'),
            ('vacuum_clean_nozzle', 'Дополнительная форсунка для подключения пылесоса'),
            ('drain_nozzle', 'Форсунка для слива воды'),
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    type_zaclad = models.CharField(
                            max_length=20,
                            choices=CHOICES_TYPE,
                            verbose_name='Категория',
                            help_text='Выбрать подходящее',
                            blank=True,
                            null=True)
    type_materials = models.CharField(
                            max_length=20,
                            choices=CHOICES,
                            default='abs',
                            verbose_name='Материал изготовления',
                            help_text='Пластик или нерж',
                            blank=True,
                            null=True)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    image = models.ImageField(upload_to='catalog/zaclad/',
                              verbose_name='Фото товара',
                              help_text='Красивое фото используется для коммерческого предложения')
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'Закладную'
        verbose_name_plural = 'Закладные'

class LightingLampModel(models.Model):
    CHOICES_LIGHT = [
            ('white', 'Белый свет'),
            ('rgb', 'RGB'),
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 blank=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    type_lighting = models.CharField(
                            max_length=20,
                            choices=CHOICES_LIGHT,
                            verbose_name='Цвет свечения',
                            help_text='Выбрать подходящее',
                            blank=True,
                            null=True)
    power = models.IntegerField(
                              verbose_name='Мощность',
                              default=0,
                              null=True,
                              blank=True,)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Лампа подводного освещения'

class LightingTransformerModel(models.Model):
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 blank=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    power = models.IntegerField(
                              verbose_name='Мощность',
                              default=0,
                              null=True,
                              blank=True,)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Понижающий трансформатор'

class LightingFlaskModel(models.Model):
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 blank=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Подводный светильник без лампы'    

class LightingAutomationModel(models.Model):
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 blank=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    power = models.IntegerField(
                              verbose_name='Мощность',
                              default=0,
                              null=True,
                              blank=True,)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Автоматика управления освещением'

class LightingAdittionalMaterialModel(models.Model):
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True,
                                 )
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Комплектующие для подводного освещения'

class LightingSetModel(models.Model):
    CHOICES = [
        ('abs', 'Пластик'),
        ('aisi', 'Нержавейка'),
        ]
    CHOICES_LIGHT = [
            ('white', 'Белый свет'),
            ('rgb', 'RGB'),
        ]
    type_materials = models.CharField(
                            max_length=20,
                            choices=CHOICES,
                            default='abs',
                            verbose_name='Материал изготовления',
                            help_text='Пластик или нерж',
                            blank=True,
                            null=True)
    type_lighting = models.CharField(
                            max_length=20,
                            choices=CHOICES_LIGHT,
                            verbose_name='Цвет свечения',
                            help_text='Выбрать подходящее',
                            blank=True,
                            null=True)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    lamp = models.ForeignKey(LightingLampModel,
                             verbose_name='Лампа',
                             help_text='Лампа для подводного освещения',
                             on_delete=models.CASCADE,
                             )
    flask = models.ForeignKey(LightingFlaskModel,
                             verbose_name='Закладная',
                             help_text='Подводный светильник',
                             on_delete=models.CASCADE,
                             )
    additional_materials = models.ManyToManyField(LightingAdittionalMaterialModel,
                                                  verbose_name='Дополнительные материалы',
                                                  help_text='Дополнительные материалы для подводного освещения',
                                                  blank=True)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Комплект подводного освещения'    

class AdditionalEquipmentHeatingModel(models.Model):

    CHOICES_TYPE = [
            ('electro', 'Электронагреватель'),
            ('warm', 'Теплообменник'),
            ('pump', 'Тепловой насос'),
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True,
                                 )
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    type_category = models.CharField(
                            max_length=20,
                            choices=CHOICES_TYPE,
                            verbose_name='Категория',
                            help_text='Выбрать подходящее',
                            blank=True,
                            null=True)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return f"{self.get_type_category_display()} / {self.name} / {self.price}"
    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Комплектующие для подогрева воды'
    

class HeatingModel(models.Model):

    CHOICES_TYPE = [
            ('electro', 'Электронагреватель'),
            ('warm', 'Теплообменник'),
            ('pump', 'Тепловой насос'),
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    type_category = models.CharField(
                            max_length=20,
                            choices=CHOICES_TYPE,
                            verbose_name='Категория',
                            help_text='Выбрать подходящее',
                            blank=True,
                            null=True)
    additional_equipment = models.ManyToManyField(AdditionalEquipmentHeatingModel,
                                                  verbose_name='Комплектующие для подключения',
                                                  help_text='Выбрать необходимое оборудование',
                                                  blank=True,
                                                  default=''
                                                  )
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    image = models.ImageField(upload_to='catalog/heating/',
                              verbose_name='Фото товара',
                              help_text='Красивое фото используется для коммерческого предложения')
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'Подогрев воды'
        verbose_name_plural = 'Подогрев воды'


class SetDesinfectionModelRX(models.Model):
    CHOICES_TYPE = [
            ('rx', 'Станция дозирования Rx'),
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из списка',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Произвольное название комплекта')
    type_category = models.CharField(
                            max_length=20,
                            choices=CHOICES_TYPE,
                            verbose_name='Категория',
                            blank=True,
                            null=True)
    rx_name = models.CharField(max_length=200,
                            verbose_name='Дозирующий насос rx',
                            help_text='В точности как у поставщика')
    rx_article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    rx_price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    rx_date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    rx_status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    rx_product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    ph_name = models.CharField(max_length=200,
                            verbose_name='Дозирующий насос РН',
                            help_text='В точности как у поставщика')
    ph_article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    ph_price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    ph_date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    ph_status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    ph_product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    rx_liquid_name = models.CharField(max_length=200,
                            verbose_name='Жидкий хлор',
                            help_text='В точности как у поставщика')
    rx_liquid_article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    rx_liquid_price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    rx_liquid_date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    rx_liquid_status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    rx_liquid_product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    ph_liquid_name = models.CharField(max_length=200,
                            verbose_name='Жидкий РН регулятор',
                            help_text='В точности как у поставщика')
    ph_liquid_article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    ph_liquid_price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    ph_liquid_date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    ph_liquid_status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    ph_liquid_product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    image = models.ImageField(upload_to='catalog/disinfection/',
                              verbose_name='Фото товара',
                              help_text='Красивое фото используется для коммерческого предложения')
    model_name = models.CharField(max_length=100, 
                                  blank=True,
                                  editable=False)
    
    def save(self, *args, **kwargs):
        if not self.model_name:
            self.model_name = self.__class__.__name__  # Получаем название модели
        super().save(*args, **kwargs)

        self.ph_liquid_price = round(self.ph_liquid_price, 2)
        self.rx_liquid_price = round(self.rx_liquid_price, 2)
        self.ph_price = round(self.ph_price, 2)
        self.rx_price = round(self.rx_price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'Комплект станции дозирования'
        verbose_name_plural = 'Дозирующее оборудование'


class SetDesinfectionModelCL(models.Model):
    CHOICES_TYPE = [
            ('cl', 'Станция дозирования с измерением свободного хлора'),
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из списка',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Произвольное название комплекта')
    type_category = models.CharField(
                            max_length=20,
                            choices=CHOICES_TYPE,
                            verbose_name='Категория',
                            blank=True,
                            null=True)
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    rx_liquid_name = models.CharField(max_length=200,
                            verbose_name='Жидкий хлор',
                            help_text='В точности как у поставщика')
    rx_liquid_article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    rx_liquid_price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    rx_liquid_date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    rx_liquid_status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    rx_liquid_product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    ph_liquid_name = models.CharField(max_length=200,
                            verbose_name='Жидкий РН регулятор',
                            help_text='В точности как у поставщика')
    ph_liquid_article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    ph_liquid_price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    ph_liquid_date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    ph_liquid_status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    ph_liquid_product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    image = models.ImageField(upload_to='catalog/disinfection/',
                              verbose_name='Фото товара',
                              help_text='Красивое фото используется для коммерческого предложения')
    model_name = models.CharField(max_length=100, 
                                  blank=True,
                                  editable=False)
    
    def save(self, *args, **kwargs):
        if not self.model_name:
            self.model_name = self.__class__.__name__  # Получаем название модели
        super().save(*args, **kwargs)

        self.ph_liquid_price = round(self.ph_liquid_price, 2)
        self.rx_liquid_price = round(self.rx_liquid_price, 2)
        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'Комплект станции дозирования с измерением свободного хлора'
        verbose_name_plural = 'Дозирубющее оборудование с измерением свободного хлора'


class HydrolysisModel(models.Model):
    CHOICES_TYPE = [
            ('h2o', 'Гидролизная установка'),
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из списка',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='В точности как у поставщика')
    type_category = models.CharField(
                            max_length=20,
                            choices=CHOICES_TYPE,
                            verbose_name='Категория',
                            blank=True,
                            null=True)
    price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    ph_liquid_name = models.CharField(max_length=200,
                            verbose_name='Жидкий РН регулятор',
                            help_text='В точности как у поставщика')
    ph_liquid_article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    ph_liquid_price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    ph_liquid_date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    ph_liquid_status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    ph_liquid_product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    image = models.ImageField(upload_to='catalog/disinfection/',
                              verbose_name='Фото товара',
                              help_text='Красивое фото используется для коммерческого предложения')
    model_name = models.CharField(max_length=100, 
                                  blank=True,
                                  editable=False)
    
    def save(self, *args, **kwargs):
        if not self.model_name:
            self.model_name = self.__class__.__name__  # Получаем название модели
        super().save(*args, **kwargs)

        self.ph_liquid_price = round(self.ph_liquid_price, 2)
        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'Гидролизная установка'
        verbose_name_plural = 'Гидролизная установка'


class DiggingModel(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Указать как будет в коммерческом предложении')
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
        verbose_name = 'Копка'
        verbose_name_plural = 'Разработка котлована'


class ExportModel(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Будет прописано в коммерческом предложении')
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
        verbose_name = 'Вывоз грунта'
        verbose_name_plural = 'Вывоз грунта'


class FittingsModel(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Будет указано в коммерческом предложении')
    price =  models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за м.')
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Арматура'
        verbose_name_plural = 'Металлопрокат'


class JobsConcretteModel(models.Model):
    CHOICES = [
            ('poly', 'Полипропилен'),
            ('pvh', 'Пленка ПВХ')
        ]
    
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Будет указано в коммерческом предложении')
    calculation = models.BooleanField(verbose_name='Участвует в расчете',
                                      help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным',
                                      default=True)
    type_pool = models.CharField(
                            max_length=20,
                            choices=CHOICES,
                            default='pvh',
                            verbose_name='Тип бассейна',
                            help_text='Пленка ПВХ / Полипропилен',
                            blank=True,
                            null=True)
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
        verbose_name = 'Работы'
        verbose_name_plural = 'Работы по бетонированию'


class EntranceModel(models.Model):
    CHOICES = [
            ('steps', 'Ступени'),
            ('ladder', 'Лестница')
        ]
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 default=0)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='Если позиция покупная то используется номенклатура. Иначе заполнить по внетреннему названию',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            help_text='В точности как в каталоге поставщика',
                            blank=True,
                            )
    type_category = models.CharField(
                            max_length=20,
                            choices=CHOICES,
                            default='steps',
                            verbose_name='Категория',
                            )
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость за ед.')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Входная группа'


class UltravioletModel(models.Model):
    supplier = models.ForeignKey(SupplierModel,
                                 verbose_name='Поставщик',
                                 help_text='Выбрать из поставщиков',
                                 blank=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=500,
                            verbose_name='Номенклатура',
                            help_text='В точности как в каталоге поставщика',
                            )
    article = models.CharField(max_length=100,
                            verbose_name='Артикул',
                            blank=True,
                            help_text='В точности как в каталоге поставщика',
                            )
    power = models.FloatField(verbose_name='Мощность',
                            help_text='Из каталога поставщика. В м3/ч',
                            default=0.00,
                            blank=True,
                            null=True)
    price = models.FloatField(default=0,
                              null=True,
                              blank=True,
                              verbose_name='Розничная стоимость')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата',
                            help_text='Дата актуальности цены',
                            null=True,
                            blank=True,
                            editable=False)
    image = models.ImageField(upload_to='catalog/pumps/',
                              verbose_name='Фото товара',
                              blank=True,
                              help_text='Красивое фото используется для коммерческого предложения')
    status = models.CharField(max_length=50,
                              default='no_found',
                              editable=False)
    product_url = models.URLField(verbose_name='Ссылка на товар у поставщика',
                                  help_text='Для актуализации цен в каталоге поставщика. ',
                                  null=True,
                                  blank=True)
    
    def save(self, *args, **kwargs):

        self.power = round(self.power, 2)
        self.price = round(self.price, 2)

        super().save(*args, **kwargs)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = 'УФ установку'
        verbose_name_plural = 'УФ установка'    

# class VacuumCleaner(models.Model):
#     brush = models.CharField(max_length=255, verbose_name="Щетка", default="Стандартная щетка")
#     rod = models.CharField(max_length=255, verbose_name="Штанга", default="Стандартная штанга")
#     hose = models.ForeignKey(Hose, on_delete=models.CASCADE, verbose_name="Шланг", related_name="vacuum_cleaners")

#     def __str__(self):
#         return f'Пылесос с {self.brush}, {self.rod}, шланг: {self.hose.length} м'
