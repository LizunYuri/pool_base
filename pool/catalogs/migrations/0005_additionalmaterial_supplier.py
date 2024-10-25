# Generated by Django 3.2 on 2024-10-23 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
        ('catalogs', '0004_auto_20241023_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalmaterial',
            name='supplier',
            field=models.ForeignKey(blank=True, default=1, help_text='Выбрать из поставщиков', on_delete=django.db.models.deletion.CASCADE, to='supplier.suppliermodel', verbose_name='Поставщик'),
            preserve_default=False,
        ),
    ]