# Generated by Django 3.2 on 2024-10-23 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0008_alter_calulaterectanglemodel_filter_element'),
    ]

    operations = [
        migrations.AddField(
            model_name='calulaterectanglemodel',
            name='filter_element_price',
            field=models.FloatField(blank=True, default=0, editable=False, help_text='Заполняется из базы', verbose_name='Цена за единицу фильтрующего эелмента'),
        ),
        migrations.AddField(
            model_name='calulaterectanglemodel',
            name='filter_element_quantity',
            field=models.FloatField(blank=True, default=0, editable=False, help_text='Заполняется из базы', verbose_name='Количество мешков'),
        ),
        migrations.AddField(
            model_name='calulaterectanglemodel',
            name='filter_element_summ',
            field=models.FloatField(blank=True, default=0, editable=False, help_text='Заполняется из базы', verbose_name='Сумма за песок'),
        ),
    ]
