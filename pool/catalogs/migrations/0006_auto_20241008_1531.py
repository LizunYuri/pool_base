# Generated by Django 3.2 on 2024-10-08 12:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_auto_20241007_1611'),
        ('catalogs', '0005_auto_20241008_1519'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lightingmodel',
            options={'verbose_name': 'Подводное освещение', 'verbose_name_plural': 'Подводное освещение'},
        ),
        migrations.CreateModel(
            name='HeatingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='В точности как в каталоге поставщика', max_length=500, verbose_name='Номенклатура')),
                ('article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('type_category', models.CharField(blank=True, choices=[('electro', 'Электронагреватель'), ('warm', 'Теплообменник'), ('pump', 'Тепловой насос')], help_text='Выбрать подходящее', max_length=20, null=True, verbose_name='Категория')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('image', models.ImageField(help_text='Красивое фото используется для коммерческого предложения', upload_to='catalog/heating/', verbose_name='Фото товара')),
                ('status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('supplier', models.ForeignKey(help_text='Выбрать из поставщиков', on_delete=django.db.models.deletion.CASCADE, to='supplier.suppliermodel', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Подогрев воды',
                'verbose_name_plural': 'Подогрев воды',
            },
        ),
        migrations.CreateModel(
            name='DisinfectionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='В точности как в каталоге поставщика', max_length=500, verbose_name='Номенклатура')),
                ('article', models.CharField(blank=True, help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('type_category', models.CharField(blank=True, choices=[('rx', 'Станция дозирования Rx'), ('ph', 'Станция дозирования PH'), ('chlorine', 'Жидкий хлор'), ('regulator', 'PH регулятор')], help_text='Выбрать подходящее', max_length=20, null=True, verbose_name='Категория')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за ед.')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('image', models.ImageField(help_text='Красивое фото используется для коммерческого предложения', upload_to='catalog/disinfection/', verbose_name='Фото товара')),
                ('status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('supplier', models.ForeignKey(help_text='Выбрать из поставщиков', on_delete=django.db.models.deletion.CASCADE, to='supplier.suppliermodel', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Дозирующее оборудование',
                'verbose_name_plural': 'Дезинфекция воды',
            },
        ),
    ]
