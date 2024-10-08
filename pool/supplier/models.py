from django.db import models

class SupplierModel(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Поставщик',
                            help_text='Название основного поставщика')
    url = models.URLField(verbose_name='Адрес каталога с ценами',
                          help_text='адрес',
                          blank=True)
    email = models.EmailField(verbose_name='Электронная почта', 
                              help_text='Электронная почта для отправки заявки',
                              blank=True)
    phone = models.CharField(max_length=20,
                             verbose_name='Номер телефона',
                             help_text='Контактный номер телефона поставщика',
                             blank=True)
    manager = models.CharField(max_length=200,
                            verbose_name='Менеджер',
                            help_text='Имя персонального менеджера',
                            blank=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
