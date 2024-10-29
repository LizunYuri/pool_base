# Generated by Django 3.2 on 2024-10-29 08:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConcreteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Будет указано в коммерческом предложении', max_length=200, verbose_name='Название')),
                ('calculation', models.BooleanField(default=True, help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным', verbose_name='Участвует в расчете')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за .м3')),
            ],
            options={
                'verbose_name': 'Бетон',
                'verbose_name_plural': 'Бетон от завода',
            },
        ),
        migrations.CreateModel(
            name='FootingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Будет указано в коммерческом предложении', max_length=200, verbose_name='Название')),
                ('calculation', models.BooleanField(default=True, help_text='По умолчанию в расчете участвует. Ели подразумевается отсутствие работ то должно быть неактивным', verbose_name='Участвует в расчете')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Розничная стоимость за .м3')),
            ],
            options={
                'verbose_name': 'Бетон',
                'verbose_name_plural': 'Бетон от завода',
            },
        ),
        migrations.CreateModel(
            name='InertMaterialsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Для отображения в коммерческом предложении', max_length=500, verbose_name='Номенклатура')),
                ('price', models.FloatField(blank=True, default=True, verbose_name='Стоимость за м3')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Инертные материалы',
            },
        ),
        migrations.CreateModel(
            name='ExcavationRequirementsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Для отображения в коммерческом предложении', max_length=500, verbose_name='Номенклатура')),
                ('construction', models.CharField(choices=[('poly', 'Полипропиленовый бассейн'), ('mosaic', 'Бетонный бассейн с покрытием мозаикой'), ('concrete', 'Бетонный бассейн с покрытием пленкой ПВХ'), ('composite', 'Композитный бассейн'), ('steel', 'Бессейн из нержавеющей стали')], default='concrete', max_length=30, verbose_name='')),
                ('filtration', models.CharField(choices=[('skimmer', 'Скиммерный бассейн'), ('overflow', 'Переливной бассейн')], default='skimmer', max_length=30, verbose_name='')),
                ('wall_thickness', models.FloatField(blank=True, help_text='в миллиметрах для расчета необходимого количества бетона', verbose_name='Толщина стен')),
                ('slab_thickness', models.FloatField(blank=True, help_text='в миллиметрах для расчета необходимого количества бетона', verbose_name='Толщина плиты')),
                ('bedding_thickness', models.FloatField(blank=True, help_text='в миллиметрах для расчета необходимого количества инертных материалов. (не обязательно)', verbose_name='Толщина подсыпки')),
                ('footing_thickness', models.FloatField(blank=True, help_text='в миллиметрах для расчета необходимого количества материалов. (не обязательно)', verbose_name='Толщина подбетонки')),
                ('reinforcement_diameter', models.FloatField(blank=True, help_text='в миллиметрах.', verbose_name='Диаметр арматуры')),
                ('cell_size', models.FloatField(blank=True, help_text='в миллиметрах для расчета необходимого количества материалов.', verbose_name='Размер ячейки')),
                ('number_of_rows', models.IntegerField(blank=True, help_text='Для расчета необходимого количества материалов.', verbose_name='Количество рядов ')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Дата актуальности цены', null=True, verbose_name='Дата')),
                ('bedding_materials', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='construction.inertmaterialsmodel', verbose_name='Материал для подсыпки')),
                ('concrete_materials', models.ForeignKey(help_text='Бетон используемый для отливки стен и основания', on_delete=django.db.models.deletion.CASCADE, to='construction.concretemodel', verbose_name='Марка бетона')),
                ('footing_materials', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='construction.footingmodel', verbose_name='Материал для подбетонки')),
            ],
            options={
                'verbose_name': 'Характеристики',
                'verbose_name_plural': 'Технические характеристики для бетнирования чаши',
            },
        ),
    ]