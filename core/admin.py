from django.contrib import admin
from .models import Branch, Warehouse, Vendor, Customer, Seller, WarehouseTransaction

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date', 'created_by', 'deleted_at']
    list_filter = ['created_date', 'deleted_at']
    search_fields = ['name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['code', 'branch', 'cash', 'created_date', 'deleted_at']
    list_filter = ['branch', 'created_date', 'deleted_at']
    search_fields = ['code', 'branch__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date', 'created_by', 'deleted_at']
    list_filter = ['created_date', 'deleted_at']
    search_fields = ['name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_date', 'deleted_at']
    list_filter = ['created_date', 'deleted_at']
    search_fields = ['name', 'phone']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'created_date', 'deleted_at']
    list_filter = ['branch', 'created_date', 'deleted_at']
    search_fields = ['name', 'branch__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(WarehouseTransaction)
class WarehouseTransactionAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'from_warehouse', 'to_warehouse', 'quantity', 'status', 'created_date']
    list_filter = ['status', 'created_date', 'from_warehouse__branch', 'to_warehouse__branch']
    search_fields = ['item_name', 'from_warehouse__code', 'to_warehouse__code']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'action_date']


