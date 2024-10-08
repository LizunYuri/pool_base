from django.db import models

class ClientModel(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='ФИО',
                            help_text='Имя клиента')
    city = models.CharField(max_length=200,
                            verbose_name='Город строительства',
                            help_text='Город строительства')
    phone = models.CharField(max_length=50,
                             verbose_name='Номер телефона клиента',
                             help_text='Номер телефона клиента')
    email = models.EmailField(verbose_name='Электронная почта',
                              help_text='Не обязательно. На указанный адрес автоматически отправится расчет',
                              blank=True)
    note = models.TextField(verbose_name='Заметка',
                            help_text='Любая информация которая может пригодится. Н обязательно к заполнению',
                            blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты компании'
