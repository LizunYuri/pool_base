# Generated by Django 3.2 on 2024-10-29 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0002_auto_20241029_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excavationrequirementsmodel',
            name='bedding_materials',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='construction.inertmaterialsmodel', verbose_name='Материал для подсыпки'),
        ),
        migrations.AlterField(
            model_name='excavationrequirementsmodel',
            name='concrete_materials',
            field=models.ForeignKey(blank=True, default='', help_text='Бетон используемый для отливки стен и основания', null=True, on_delete=django.db.models.deletion.CASCADE, to='construction.concretemodel', verbose_name='Марка бетона'),
        ),
        migrations.AlterField(
            model_name='excavationrequirementsmodel',
            name='construction',
            field=models.CharField(choices=[('poly', 'Полипропиленовый бассейн'), ('mosaic', 'Бетонный бассейн с покрытием мозаикой'), ('pvh', 'Бетонный бассейн с покрытием пленкой ПВХ'), ('composite', 'Композитный бассейн'), ('steel', 'Бессейн из нержавеющей стали')], default='pvh', max_length=30, verbose_name='тип бассейна'),
        ),
        migrations.AlterField(
            model_name='excavationrequirementsmodel',
            name='footing_materials',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='construction.footingmodel', verbose_name='Материал для подбетонки'),
        ),
    ]
