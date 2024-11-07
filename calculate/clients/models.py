from django.db import models
from django.contrib.auth.models import User

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
    responsible = models.ForeignKey(User,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True)

    def save(self, *args, **kwargs):
        # Получаем текущего пользователя из kwargs, если передан
        if 'user' in kwargs and not self.responsible:
            self.responsible = kwargs.pop('user')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты компании'
