import os
from django.db import models
from django.contrib.auth.models import User


class Phones(models.Model):
    phone = models.CharField(max_length=20,
                             verbose_name='Номер телефона',
                             help_text='Контактный номер телефона')
    name = models.CharField(max_length=200,
                            verbose_name='Менеджер',)
    
    def __str__(self): 
        return self.name
    
    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Номера телефонов компании'        



class Company(models.Model):
    personal = models.ManyToManyField(to=User,
                                    blank=True)
    default = models.BooleanField(verbose_name='Использовать по умолчанию',
                                    default=False,
                                    editable=False)
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Коммерческое название компании')
    legal_name = models.CharField(max_length=200,
                            verbose_name='Юридическое название',
                            help_text='ООО или ИП')
    inn = models.IntegerField(help_text='ИНН',
                              verbose_name='ИНН'
                              )
    ogrn = models.IntegerField(help_text='ОГРН',
                              verbose_name='ОГРН'
                              )
    post_address = models.TextField(verbose_name='Юридиченский адрес',
                                    help_text='Для договора')
    physical_address = models.TextField(verbose_name='Фактический адрес',
                                    help_text='Для договора')
    phone = models.ManyToManyField(to=Phones,
                             verbose_name='Номер телефона',
                             help_text='Контактный номер телефона')
    email = models.EmailField(max_length=254,
                              verbose_name='Адрес электронной почты',
                              )
    web_site = models.CharField(max_length=200,
                                verbose_name='Веб сайт',
                                help_text='при наличии',
                                default='',
                                blank=True)
    logotype = models.ImageField(verbose_name='Логотип компании ',
                                upload_to='company/logotype/',
                                help_text='Без заднего фона',
                                blank=True)

    def __str__(self): 
        return self.name
    
    def delete(self, *args, **kwargs):
        # Удаление файла изображения
        if self.logotype and os.path.isfile(self.logotype.path):
            os.remove(self.logotype.path)
        super().delete(*args, **kwargs)

    def get_image_url(self):
        if self.logotype:
            return self.logotype.url
        return None
    
    class Meta:
        verbose_name = 'Компанию'
        verbose_name_plural = 'Данные компании'

User.add_to_class('__str__', lambda self: f'{self.first_name} {self.last_name}')

