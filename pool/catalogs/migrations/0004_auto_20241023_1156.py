# Generated by Django 3.2 on 2024-10-23 08:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0003_alter_filtermodel_valve'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Как в каталоге поставщика', max_length=200, verbose_name='Наименование')),
                ('unit_of_measurement', models.CharField(blank=True, choices=[('psc', 'шт.'), ('m_ch', 'м/пог'), ('m_2', 'м2'), ('kg', 'кг')], default='psc', max_length=20, null=True, verbose_name='Единица измерения')),
                ('type_material', models.CharField(help_text='Максимально приближенная', max_length=20, verbose_name='Категория')),
                ('price', models.FloatField(default=0, verbose_name='Цена за единицу')),
                ('status', models.CharField(default='no_found', editable=False, max_length=50)),
                ('product_url', models.URLField(blank=True, help_text='Для актуализации цен в каталоге поставщика. ', null=True, verbose_name='Ссылка на товар у поставщика')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Номенклатуру',
                'verbose_name_plural': 'Дополнительные материалы для отделки чаши бассейна',
            },
        ),
        migrations.AddField(
            model_name='finishingmaterialsmodel',
            name='additional_materials',
            field=models.ManyToManyField(blank=True, to='catalogs.AdditionalMaterial', verbose_name='Дополнительные материалы'),
        ),
    ]
