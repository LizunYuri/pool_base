# Generated by Django 3.2 on 2024-10-17 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0009_alter_calulaterectanglemodel_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calulaterectanglemodel',
            name='finished_materials',
            field=models.CharField(editable=False, help_text='Финишная отделка', max_length=200, verbose_name='Материал'),
        ),
    ]
