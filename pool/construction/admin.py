from django.contrib import admin
from .models import ConcreteModel, InertMaterialsModel, ExcavationRequirementsModel, FootingModel

@admin.register(ExcavationRequirementsModel)
class ExcavationRequirementsModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name',  )
    search_fields = ('name', )

@admin.register(InertMaterialsModel)
class InertMaterialsModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name',  )
    search_fields = ('name', )

@admin.register(ConcreteModel)
class ConcreteModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name', )

@admin.register(FootingModel)
class FootingModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name', )