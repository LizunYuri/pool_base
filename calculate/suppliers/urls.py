from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path('get-supplier/', views.get_suppliers, name='get-suppliers'),
    path('suppliers-list/', views.suppliers_list, name='suppliers-list'),
    path('supplier/<int:supplier_id>/', views.supplier_detail, name='supplier-detail'),
    path('supplier/<int:supplier_id>/delete/', views.delete_supplier, name='delete-supplier'),
    path('supplier/<int:supplier_id>/edit/', views.edit_supplier, name='supplier-edit'),
    path('create/', views.create_supplier, name='supplier-create'),
    path('search/', views.search_supplier, name='search-supplier'),
    ]
