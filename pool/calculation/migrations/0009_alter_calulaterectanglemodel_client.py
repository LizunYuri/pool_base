# Generated by Django 3.2 on 2024-10-17 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_remove_clientmodel_send_calculation'),
        ('calculation', '0008_auto_20241017_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calulaterectanglemodel',
            name='client',
            field=models.ForeignKey(help_text='Обязательно к заполнению', on_delete=django.db.models.deletion.CASCADE, to='clients.clientmodel', verbose_name='Клиент'),
        ),
    ]
