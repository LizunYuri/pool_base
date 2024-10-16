# Generated by Django 3.2 on 2024-10-08 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0005_auto_20241008_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calulaterectanglemodel',
            name='water_exchange_time',
            field=models.FloatField(choices=[(6.0, '6 часов'), (4.0, '4 часа'), (2.0, '2 часа'), (1.0, '1 час'), (0.5, '30 минут')], default=4, help_text='Для частного бассейна необходимо 6 часов, для бассейнов в небольших гостиницах 4 часа', max_length=20, verbose_name='Время полного водообмена'),
        ),
    ]
