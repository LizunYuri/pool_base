from django.contrib import admin
from .models import ClientModel

@admin.register(ClientModel)
class ClientModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone')
    list_filter = ('name', 'city', 'phone')
    search_fields = ('name', 'city', 'phone')