# Generated by Django 3.2 on 2024-10-23 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0007_filterelementmodel'),
        ('calculation', '0004_auto_20241023_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='calulaterectanglemodel',
            name='filter_element',
            field=models.ForeignKey(default=1, help_text='Выбрать из имеющегося', on_delete=django.db.models.deletion.CASCADE, to='catalogs.filterelementmodel', verbose_name='Фильтрующий элемент'),
            preserve_default=False,
        ),
    ]
