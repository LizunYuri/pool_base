# Generated by Django 3.2 on 2024-10-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, help_text='адрес', verbose_name='Адрес каталога с ценами')),
                ('email', models.EmailField(blank=True, help_text='Электронная почта для отправки заявки', max_length=254, verbose_name='Электронная почта')),
                ('phone', models.CharField(blank=True, help_text='Контактный номер телефона поставщика', max_length=20, verbose_name='Номер телефона')),
                ('name', models.CharField(blank=True, help_text='Имя персонального менеджера', max_length=200, verbose_name='Менеджер')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
    ]
