# Generated by Django 3.2 on 2024-10-18 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0013_concretemodel_diggingmodel_exportmodel_fittingsmodel_jobsconcrettemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='concretemodel',
            name='calculation',
            field=models.BooleanField(default=True, help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным', verbose_name='Участвует в расчете'),
        ),
        migrations.AddField(
            model_name='diggingmodel',
            name='calculation',
            field=models.BooleanField(default=True, help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным', verbose_name='Участвует в расчете'),
        ),
        migrations.AddField(
            model_name='exportmodel',
            name='calculation',
            field=models.BooleanField(default=True, help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным', verbose_name='Участвует в расчете'),
        ),
        migrations.AddField(
            model_name='jobsconcrettemodel',
            name='calculation',
            field=models.BooleanField(default=True, help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным', verbose_name='Участвует в расчете'),
        ),
    ]