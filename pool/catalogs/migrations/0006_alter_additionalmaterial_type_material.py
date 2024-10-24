# Generated by Django 3.2 on 2024-10-23 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0005_additionalmaterial_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalmaterial',
            name='type_material',
            field=models.CharField(choices=[('corner', 'Угол с напылением ПВХ'), ('textile', 'Геотекстиль'), ('glue', 'Клей для геотекстиля'), ('pvc_glue', 'Жидкий ПВХ')], help_text='Максимально приближенная', max_length=20, verbose_name='Категория'),
        ),
    ]
