from django.contrib import admin
from .models import GoldInvoice, GoldInvoiceItem, SilverInvoice, SilverInvoiceItem

class GoldInvoiceItemInline(admin.TabularInline):
    model = GoldInvoiceItem
    extra = 1
    readonly_fields = ['item_total_price']

@admin.register(GoldInvoice)
class GoldInvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'seller', 'branch', 'total_price', 'invoice_type', 'transaction_type', 'created_date']
    list_filter = ['invoice_type', 'transaction_type', 'branch', 'created_date']
    search_fields = ['customer__name', 'seller__name', 'branch__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'total_price']
    inlines = [GoldInvoiceItemInline]

@admin.register(GoldInvoiceItem)
class GoldInvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'item_name', 'vendor_name', 'item_quantity', 'item_weight', 'item_carat', 'item_total_price']
    list_filter = ['vendor_name', 'item_carat']
    search_fields = ['item_name', 'vendor_name', 'invoice__customer__name']
    readonly_fields = ['item_total_price']

class SilverInvoiceItemInline(admin.TabularInline):
    model = SilverInvoiceItem
    extra = 1
    readonly_fields = ['item_total_price']

@admin.register(SilverInvoice)
class SilverInvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'seller', 'branch', 'total_price', 'invoice_type', 'transaction_type', 'created_date']
    list_filter = ['invoice_type', 'transaction_type', 'branch', 'created_date']
    search_fields = ['customer__name', 'seller__name', 'branch__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'total_price']
    inlines = [SilverInvoiceItemInline]

@admin.register(SilverInvoiceItem)
class SilverInvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'item_name', 'vendor_name', 'item_quantity', 'item_weight', 'item_carat', 'item_total_price']
    list_filter = ['vendor_name', 'item_carat']
    search_fields = ['item_name', 'vendor_name', 'invoice__customer__name']
    readonly_fields = ['item_total_price']