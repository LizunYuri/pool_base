# Generated by Django 3.2 on 2024-10-18 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0012_auto_20241018_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcreteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Будет указано в коммерческом предложении', max_length=200, verbose_name='Название')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за .м3')),
            ],
            options={
                'verbose_name': 'Бетон',
                'verbose_name_plural': 'Бетон от завода',
            },
        ),
        migrations.CreateModel(
            name='DiggingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Указать как будет в коммерческом предложении', max_length=200, verbose_name='Название')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за .м3')),
            ],
            options={
                'verbose_name': 'Копка',
                'verbose_name_plural': 'Разработка котлована',
            },
        ),
        migrations.CreateModel(
            name='ExportModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Будет прописано в коммерческом предложении', max_length=200, verbose_name='Название')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за .м3')),
            ],
            options={
                'verbose_name': 'Вывоз грунта',
                'verbose_name_plural': 'Вывоз грунта',
            },
        ),
        migrations.CreateModel(
            name='FittingsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Будет указано в коммерческом предложении', max_length=200, verbose_name='Название')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за м.')),
            ],
            options={
                'verbose_name': 'Арматура',
                'verbose_name_plural': 'Металлопрокат',
            },
        ),
        migrations.CreateModel(
            name='JobsConcretteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Будет указано в коммерческом предложении', max_length=200, verbose_name='Название')),
                ('type_pool', models.CharField(blank=True, choices=[('poly', 'Полипропилен'), ('pvh', 'Пленка ПВХ')], default='pvh', help_text='Пленка ПВХ / Полипропилен', max_length=20, null=True, verbose_name='Тип бассейна')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за .м3')),
            ],
            options={
                'verbose_name': 'Работы',
                'verbose_name_plural': 'Работы по бетонированию',
            },
        ),
    ]