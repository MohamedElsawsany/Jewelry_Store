from django.contrib import admin
from .models import GoldProduct, SilverProduct, GoldWarehouseStock, SilverWarehouseStock

@admin.register(GoldProduct)
class GoldProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'weight', 'carat', 'stamp_enduser', 'created_date', 'deleted_at']
    list_filter = ['vendor', 'carat', 'created_date', 'deleted_at']
    search_fields = ['name', 'vendor__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(SilverProduct)
class SilverProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'weight', 'carat', 'stamp_enduser', 'created_date', 'deleted_at']
    list_filter = ['vendor', 'carat', 'created_date', 'deleted_at']
    search_fields = ['name', 'vendor__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(GoldWarehouseStock)
class GoldWarehouseStockAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'created_date', 'deleted_at']
    list_filter = ['warehouse', 'warehouse__branch', 'created_date', 'deleted_at']
    search_fields = ['product__name', 'warehouse__code']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(SilverWarehouseStock)
class SilverWarehouseStockAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'created_date', 'deleted_at']
    list_filter = ['warehouse', 'warehouse__branch', 'created_date', 'deleted_at']
    search_fields = ['product__name', 'warehouse__code']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']