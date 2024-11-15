# Generated by Django 5.1.3 on 2024-11-14 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliermodel',
            name='legal_name',
            field=models.CharField(blank=True, help_text='Для оформления заказа поставщику', max_length=200, verbose_name='Юридическое наименование'),
        ),
    ]