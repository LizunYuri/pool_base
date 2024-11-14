from django.contrib import admin
from .models import SupplierModel

@admin.register(SupplierModel)
class SupplierModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_filter  = ('name', 'url')
    search_fields  = ('name', 'url')