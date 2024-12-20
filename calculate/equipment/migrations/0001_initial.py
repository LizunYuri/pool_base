# Generated by Django 3.2 on 2024-11-12 13:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PumpsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='В точности как в каталоге поставщика', max_length=500, verbose_name='Номенклатура')),
                ('article', models.CharField(help_text='В точности как в каталоге поставщика', max_length=100, verbose_name='Артикул')),
                ('power', models.FloatField(blank=True, default=0.0, help_text='Из каталога поставщика. В м3/ч', null=True, verbose_name='Мощность')),
                ('voltage', models.CharField(blank=True, choices=[('220v', '220v'), ('380v', '380v')], default='220v', help_text='220 Вольт / 380вольт', max_length=20, null=True, verbose_name='Вольтаж')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('image', models.ImageField(blank=True, help_text='Красивое фото используется для коммерческого предложения', null=True, upload_to='catalog/pumps/', verbose_name='Фото товара')),
                ('status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
            ],
            options={
                'verbose_name': 'Насос',
                'verbose_name_plural': 'Насосное оборудование',
            },
        ),
    ]
