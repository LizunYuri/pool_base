# Generated by Django 3.2 on 2024-10-17 11:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_auto_20241007_1611'),
        ('catalogs', '0006_auto_20241008_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='HydrolysisModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='В точности как у поставщика', max_length=200, verbose_name='Название')),
                ('type_category', models.CharField(blank=True, choices=[('h2o', 'Гидролизная установка')], max_length=20, null=True, verbose_name='Категория')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('ph_liquid_name', models.CharField(help_text='В точности как у поставщика', max_length=200, verbose_name='Жидкий РН регулятор')),
                ('ph_liquid_article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('phliquid_liquid_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('ph_liquid_date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('ph_liquid_status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('ph_liquid_product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('image', models.ImageField(help_text='Красивое фото используется для коммерческого предложения', upload_to='catalog/disinfection/', verbose_name='Фото товара')),
                ('supplier', models.ForeignKey(help_text='Выбрать из списка', on_delete=django.db.models.deletion.CASCADE, to='supplier.suppliermodel', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Гидролизная установка',
                'verbose_name_plural': 'Гидролизная установка',
            },
        ),
        migrations.CreateModel(
            name='SetDesinfectionModelCL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Произвольное название комплекта', max_length=200, verbose_name='Название')),
                ('type_category', models.CharField(blank=True, choices=[('cl', 'Станция дозирования с измерением свободного хлора')], max_length=20, null=True, verbose_name='Категория')),
                ('rx_name', models.CharField(help_text='В точности как у поставщика', max_length=200, verbose_name='Станция дозирования с измерением свободного хлора')),
                ('rx_article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('rx_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('rx_date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('rx_status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('rx_product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('rx_liquid_name', models.CharField(help_text='В точности как у поставщика', max_length=200, verbose_name='Жидкий хлор')),
                ('rx_liquid_article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('rx_liquid_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('rx_liquid_date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('rx_liquid_status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('rx_liquid_product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('ph_liquid_name', models.CharField(help_text='В точности как у поставщика', max_length=200, verbose_name='Жидкий РН регулятор')),
                ('ph_liquid_article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('phliquid_liquid_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('ph_liquid_date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('ph_liquid_status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('ph_liquid_product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('image', models.ImageField(help_text='Красивое фото используется для коммерческого предложения', upload_to='catalog/disinfection/', verbose_name='Фото товара')),
                ('supplier', models.ForeignKey(help_text='Выбрать из списка', on_delete=django.db.models.deletion.CASCADE, to='supplier.suppliermodel', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Комплект станции дозирования с измерением свободного хлора',
                'verbose_name_plural': 'Дозирубющее оборудование с измерением свободного хлора',
            },
        ),
        migrations.CreateModel(
            name='SetDesinfectionModelRX',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Произвольное название комплекта', max_length=200, verbose_name='Название')),
                ('type_category', models.CharField(blank=True, choices=[('rx', 'Станция дозирования Rx')], max_length=20, null=True, verbose_name='Категория')),
                ('rx_name', models.CharField(help_text='В точности как у поставщика', max_length=200, verbose_name='Дозирующий насос rx')),
                ('rx_article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('rx_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('rx_date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('rx_status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('rx_product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('ph_name', models.CharField(help_text='В точности как у поставщика', max_length=200, verbose_name='Дозирующий насос РН')),
                ('ph_article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('ph_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('ph_date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('ph_status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('ph_product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('rx_liquid_name', models.CharField(help_text='В точности как у поставщика', max_length=200, verbose_name='Жидкий хлор')),
                ('rx_liquid_article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('rx_liquid_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('rx_liquid_date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('rx_liquid_status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('rx_liquid_product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('ph_liquid_name', models.CharField(help_text='В точности как у поставщика', max_length=200, verbose_name='Жидкий РН регулятор')),
                ('ph_liquid_article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('phliquid_liquid_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('ph_liquid_date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('ph_liquid_status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('ph_liquid_product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('image', models.ImageField(help_text='Красивое фото используется для коммерческого предложения', upload_to='catalog/disinfection/', verbose_name='Фото товара')),
                ('supplier', models.ForeignKey(help_text='Выбрать из списка', on_delete=django.db.models.deletion.CASCADE, to='supplier.suppliermodel', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Комплект станции дозирования',
                'verbose_name_plural': 'Дозирующее оборудование',
            },
        ),
        migrations.DeleteModel(
            name='DisinfectionModel',
        ),
    ]