import os
from django.utils import timezone
from django.db import models
from supplier.models import SupplierModel



class FilterModel(models.Model):
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
            ('scimmer', 'Скиммер'),
            ('forsunka', 'Возвратная фрсунка'),
            ('sliv', 'Донный слив'),
            ('doliv', 'Долив воды'),
            ('polusos', 'Пылесос'),
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


class LightingModel(models.Model):
    CHOICES = [
            ('abs', 'ABS пластик'),
            ('aisi', 'AISI-316 нержавеющий металл')
        ]
    CHOICES_TYPE = [
            ('lamp', 'Лампа'),
            ('flask', 'Прожектор без лампы'),
            ('overlay', 'Лицевая панель'),
            ('automation', 'Автоматика управления'),
        ]
    CHOICES_LIGHT = [
            ('white', 'Белый свет'),
            ('rgb', 'RGB'),
            ('none', 'НЕТ (Для закладной и автоматики)'),
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
    type_lighting = models.CharField(
                            max_length=20,
                            choices=CHOICES_LIGHT,
                            verbose_name='Цвет свечения',
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
    image = models.ImageField(upload_to='catalog/light/',
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
        verbose_name = 'Подводное освещение'
        verbose_name_plural = 'Подводное освещение'


class DisinfectionModel(models.Model):

    CHOICES_TYPE = [
            ('rx', 'Станция дозирования Rx'),
            ('ph', 'Станция дозирования PH'),
            ('chlorine', 'Жидкий хлор'),
            ('regulator', 'PH регулятор'),
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
    image = models.ImageField(upload_to='catalog/disinfection/',
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
        verbose_name = 'Дозирующее оборудование'
        verbose_name_plural = 'Дезинфекция воды'


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