from rest_framework import serializers
from .models import GoldInvoice, GoldInvoiceItem, SilverInvoice, SilverInvoiceItem

class GoldInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldInvoiceItem
        fields = ['id', 'item_name', 'item_weight', 'item_carat', 'item_stamp_enduser',
                 'item_quantity', 'item_price', 'item_total_price', 'vendor_name']

class GoldInvoiceSerializer(serializers.ModelSerializer):
    items = GoldInvoiceItemSerializer(many=True, read_only=True)
    warehouse_code = serializers.CharField(source='warehouse.code', read_only=True)
    seller_name = serializers.CharField(source='seller.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = GoldInvoice
        fields = ['id', 'warehouse', 'warehouse_code', 'seller', 'seller_name', 
                 'branch', 'branch_name', 'customer', 'customer_name', 'customer_phone',
                 'gold_price_21', 'gold_price_24', 'total_price', 'transaction_type',
                 'invoice_type', 'created_date', 'updated_date', 'created_by', 
                 'created_by_username', 'items']
        read_only_fields = ['id', 'total_price', 'created_date', 'updated_date', 'created_by_username']

class GoldInvoiceCreateSerializer(serializers.ModelSerializer):
    items = GoldInvoiceItemSerializer(many=True)
    
    class Meta:
        model = GoldInvoice
        fields = ['warehouse', 'seller', 'branch', 'customer', 'gold_price_21', 
                 'gold_price_24', 'transaction_type', 'invoice_type', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = GoldInvoice.objects.create(**validated_data)
        
        total_price = 0
        for item_data in items_data:
            item = GoldInvoiceItem.objects.create(invoice=invoice, **item_data)
            total_price += item.item_total_price
        
        invoice.total_price = total_price
        invoice.save()
        return invoice

class SilverInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SilverInvoiceItem
        fields = ['id', 'item_name', 'item_weight', 'item_carat', 'item_stamp_enduser',
                 'item_quantity', 'item_price', 'item_total_price', 'vendor_name']

class SilverInvoiceSerializer(serializers.ModelSerializer):
    items = SilverInvoiceItemSerializer(many=True, read_only=True)
    warehouse_code = serializers.CharField(source='warehouse.code', read_only=True)
    seller_name = serializers.CharField(source='seller.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = SilverInvoice
        fields = ['id', 'warehouse', 'warehouse_code', 'seller', 'seller_name', 
                 'branch', 'branch_name', 'customer', 'customer_name', 'customer_phone',
                 'silver_price', 'total_price', 'transaction_type', 'invoice_type', 
                 'created_date', 'updated_date', 'created_by', 'created_by_username', 'items']
        read_only_fields = ['id', 'total_price', 'created_date', 'updated_date', 'created_by_username']

class SilverInvoiceCreateSerializer(serializers.ModelSerializer):
    items = SilverInvoiceItemSerializer(many=True)
    
    class Meta:
        model = SilverInvoice
        fields = ['warehouse', 'seller', 'branch', 'customer', 'silver_price', 
                 'transaction_type', 'invoice_type', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = SilverInvoice.objects.create(**validated_data)
        
        total_price = 0
        for item_data in items_data:
            item = SilverInvoiceItem.objects.create(invoice=invoice, **item_data)
            total_price += item.item_total_price
        
        invoice.total_price = total_price
        invoice.save()
        return invoice

# Report Serializers
class InvoiceSummarySerializer(serializers.Serializer):
    invoice_type = serializers.CharField()
    transaction_type = serializers.CharField()
    count = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2)

class DailySalesSerializer(serializers.Serializer):
    date = serializers.DateField()
    gold_sales = serializers.DecimalField(max_digits=15, decimal_places=2)
    silver_sales = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_sales = serializers.DecimalField(max_digits=15, decimal_places=2)