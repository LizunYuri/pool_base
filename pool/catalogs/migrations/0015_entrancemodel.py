# Generated by Django 3.2 on 2024-10-18 10:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_auto_20241007_1611'),
        ('catalogs', '0014_auto_20241018_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Если позиция покупная то используется номенклатура. Иначе заполнить по внетреннему названию', max_length=500, verbose_name='Номенклатура')),
                ('article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('type_category', models.CharField(blank=True, choices=[('steps', 'Ступени'), ('ladder', 'Лестница')], default='pvh', max_length=20, null=True, verbose_name='Категория')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('supplier', models.ForeignKey(blank=True, help_text='Выбрать из поставщиков', on_delete=django.db.models.deletion.CASCADE, to='supplier.suppliermodel', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Номенклатуру',
                'verbose_name_plural': 'Входная группа',
            },
        ),
    ]
