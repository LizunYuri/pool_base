from django.contrib import admin
from .models import FilterModel, PumpsModel, FinishingMaterialsModel, ZacladModel, LightingModel, DisinfectionModel, HeatingModel


@admin.register(FilterModel)
class FilterModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(PumpsModel)
class PumpsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(FinishingMaterialsModel)
class FinishingMaterialsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(ZacladModel)
class ZacladModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(LightingModel)
class LightingModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(DisinfectionModel)
class DisinfectionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')
    
@admin.register(HeatingModel)
class HeatingModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')