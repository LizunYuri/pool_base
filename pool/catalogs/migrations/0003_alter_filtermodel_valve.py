# Generated by Django 3.2 on 2024-10-23 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0002_filtermodel_valve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtermodel',
            name='valve',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Тип вентиля'),
        ),
    ]