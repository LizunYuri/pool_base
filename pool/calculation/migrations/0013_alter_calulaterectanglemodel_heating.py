# Generated by Django 3.2 on 2024-10-17 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0012_alter_calulaterectanglemodel_ligth_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calulaterectanglemodel',
            name='heating',
            field=models.CharField(blank=True, editable=False, help_text='Подогрев воды в бассейне', max_length=200, null=True, verbose_name='Подогрев'),
        ),
    ]
