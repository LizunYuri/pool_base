from django.contrib import admin
from .models import Phones, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'legal_name', 'inn', 'ogrn', 'default')
    list_filter = ('name', 'legal_name', 'inn', 'ogrn')
    search_fields = ('name', 'legal_name', 'inn', 'ogrn')

@admin.register(Phones)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    list_filter = ('name', 'phone')
    search_fields = ('name', 'phone')