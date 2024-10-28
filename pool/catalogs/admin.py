from django.contrib import admin
from .models import LightingAutomationModel, LightingFlaskModel, LightingLampModel, LightingSetModel, LightingTransformerModel, LightingAdittionalMaterialModel, UltravioletModel, AdditionalEquipmentHeatingModel, ValveGroupModel, WorkMaterialModel, FilterElementModel, AdditionalMaterial, ConcreteModel, EntranceModel, ExportModel, JobsConcretteModel, DiggingModel, FilterModel, PumpsModel, FinishingMaterialsModel, ZacladModel, HeatingModel, SetDesinfectionModelCL, SetDesinfectionModelRX, HydrolysisModel


@admin.register(LightingSetModel)
class LightingSetModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name',  )
    search_fields = ('name', )

@admin.register(LightingAutomationModel)
class LightingAutomationModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(LightingFlaskModel)
class LightingFlaskModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(LightingLampModel)
class LightingLampModelAdmin(admin.ModelAdmin):
    list_display = ('name',  'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(LightingTransformerModel)
class LightingTransformerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(LightingAdittionalMaterialModel)
class LightingAdittionalMaterialModelAdmin(admin.ModelAdmin):
    list_display = ('name',  'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')


@admin.register(AdditionalEquipmentHeatingModel)
class AdditionalEquipmentHeating(admin.ModelAdmin):
    list_display = ('name', 'type_category', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(FilterModel)
class FilterModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')

@admin.register(ValveGroupModel)
class ValveGroupModelAdmin(admin.ModelAdmin):
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

@admin.register(WorkMaterialModel)
class WorkMaterialModelAdmin(admin.ModelAdmin):
    list_display = ('name',  'price', 'unit_of_measurement')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')

@admin.register(AdditionalMaterial)
class AdditionalMaterialAdmin(admin.ModelAdmin):
    list_display = ('type_material', 'name', 'unit_of_measurement', 'price')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')


@admin.register(FilterElementModel)
class FilterElementModelAdmin(admin.ModelAdmin):
    list_display = ('name','price')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')

@admin.register(UltravioletModel)
class UltravioletModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'supplier')
    list_filter = ('name', 'price', 'date', 'supplier')
    search_fields = ('name', 'price', 'date', 'supplier')