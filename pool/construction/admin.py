from django.contrib import admin
from .models import ReinforcementModel, ConcreteModel, InertMaterialsModel, ExcavationRequirementsModel, FootingModel, ExcavationJobsModel

@admin.register(ExcavationRequirementsModel)
class ExcavationRequirementsModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name',  )
    search_fields = ('name', )

@admin.register(ExcavationJobsModel)
class ExcavationJobsModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name',  )
    search_fields = ('name', )

@admin.register(ReinforcementModel)
class ReinforcementModelAdmin(admin.ModelAdmin):
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