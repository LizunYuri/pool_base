from django.contrib import admin
from .models import ConcreteModel, EntranceModel, ExportModel, JobsConcretteModel, DiggingModel, FilterModel, PumpsModel, FinishingMaterialsModel, ZacladModel, LightingModel, HeatingModel, SetDesinfectionModelCL, SetDesinfectionModelRX, HydrolysisModel


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

@admin.register(DiggingModel)
class DiggingModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')

@admin.register(ConcreteModel)
class ConcreteModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')

@admin.register(ExportModel)
class ExportModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')

@admin.register(JobsConcretteModel)
class ExportModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_pool', 'price')
    list_filter = ('name', 'type_pool', 'price')
    search_fields = ('name', 'type_pool', 'price')

@admin.register(EntranceModel)
class EntranceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_category', 'price')
    list_filter = ('name', 'type_category', 'price')
    search_fields = ('name', 'type_category', 'price')
