# Generated by Django 5.1.3 on 2024-11-14 08:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
        ('suppliers', '0002_suppliermodel_legal_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pumpsmodel',
            name='supplier',
            field=models.ForeignKey(default=1, help_text='Выбрать из поставщиков', on_delete=django.db.models.deletion.CASCADE, to='suppliers.suppliermodel', verbose_name='Поставщик'),
            preserve_default=False,
        ),
    ]