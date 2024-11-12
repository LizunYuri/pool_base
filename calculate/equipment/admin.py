from django.contrib import admin
from .models import PumpsModel

# Register your models here.
@admin.register(PumpsModel)
class PumpsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date')
    list_filter = ('name', 'price', 'date')
    search_fields = ('name', 'price', 'date')
