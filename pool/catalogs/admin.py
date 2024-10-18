from django.contrib import admin
from .models import FilterModel, PumpsModel, FinishingMaterialsModel, ZacladModel, LightingModel, HeatingModel, SetDesinfectionModelCL, SetDesinfectionModelRX, HydrolysisModel


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
 
@admin.register(HeatingModel)
class HeatingModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(SetDesinfectionModelRX)
class SetDesinfectionModelRXAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    list_filter = ('name',  'supplier')
    search_fields = ('name', 'supplier')

@admin.register(SetDesinfectionModelCL)
class SetDesinfectionModelCLAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    list_filter = ('name', 'supplier')
    search_fields = ('name', 'supplier')


@admin.register(HydrolysisModel)
class HydrolysisModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    list_filter = ('name', 'date', 'supplier')
    search_fields = ('name', 'supplier')