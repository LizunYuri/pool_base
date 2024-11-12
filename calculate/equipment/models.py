import os
from django.utils import timezone
from django.db import models



class PumpsModel(models.Model):
    CHOICES = [
            ('220v', '220v'),
            ('380v', '380v')
        ]
    # supplier = models.ForeignKey(SupplierModel,
    #                              verbose_name='Поставщик',
    #                              help_text='Выбрать из поставщиков',
    #                              on_delete=models.CASCADE)
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
                            null=True,
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
        verbose_name = 'Насос'
        verbose_name_plural = 'Насосное оборудование'

