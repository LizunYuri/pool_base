# Generated by Django 3.2 on 2024-10-17 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0008_rename_phliquid_liquid_price_setdesinfectionmodelrx_ph_liquid_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hydrolysismodel',
            old_name='phliquid_liquid_price',
            new_name='ph_liquid_price',
        ),
        migrations.RenameField(
            model_name='setdesinfectionmodelcl',
            old_name='phliquid_liquid_price',
            new_name='ph_liquid_price',
        ),
    ]