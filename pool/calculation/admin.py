from django.contrib import admin
from .models import CalulateRectangleModel

@admin.register(CalulateRectangleModel)
class CalulateRectangleModelAdmin(admin.ModelAdmin):
    list_display = ('client',)
    list_filter = ('client',)
    search_fields = ('client',)
# Register your models here.
