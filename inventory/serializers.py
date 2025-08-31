from rest_framework import serializers
from .models import GoldProduct, SilverProduct, GoldWarehouseStock, SilverWarehouseStock

class GoldProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = GoldProduct
        fields = ['id', 'vendor', 'vendor_name', 'name', 'weight', 'carat', 
                 'stamp_enduser', 'cashback', 'cashback_unpacking', 'created_date', 
                 'updated_date', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'updated_date', 'created_by_username']

class SilverProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = SilverProduct
        fields = ['id', 'vendor', 'vendor_name', 'name', 'weight', 'carat', 
                 'stamp_enduser', 'cashback', 'cashback_unpacking', 'created_date', 
                 'updated_date', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'updated_date', 'created_by_username']

class GoldWarehouseStockSerializer(serializers.ModelSerializer):
    warehouse_code = serializers.CharField(source='warehouse.code', read_only=True)
    warehouse_branch = serializers.CharField(source='warehouse.branch.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_weight = serializers.DecimalField(source='product.weight', max_digits=10, decimal_places=2, read_only=True)
    product_carat = serializers.DecimalField(source='product.carat', max_digits=10, decimal_places=2, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = GoldWarehouseStock
        fields = ['id', 'warehouse', 'warehouse_code', 'warehouse_branch', 
                 'product', 'product_name', 'product_weight', 'product_carat',
                 'quantity', 'created_date', 'updated_date', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'updated_date', 'created_by_username']

class SilverWarehouseStockSerializer(serializers.ModelSerializer):
    warehouse_code = serializers.CharField(source='warehouse.code', read_only=True)
    warehouse_branch = serializers.CharField(source='warehouse.branch.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_weight = serializers.DecimalField(source='product.weight', max_digits=10, decimal_places=2, read_only=True)
    product_carat = serializers.DecimalField(source='product.carat', max_digits=10, decimal_places=2, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = SilverWarehouseStock
        fields = ['id', 'warehouse', 'warehouse_code', 'warehouse_branch', 
                 'product', 'product_name', 'product_weight', 'product_carat',
                 'quantity', 'created_date', 'updated_date', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'updated_date', 'created_by_username']

# Stock Summary Serializers
class GoldStockSummarySerializer(serializers.Serializer):
    warehouse = serializers.CharField()
    warehouse_code = serializers.CharField()
    total_products = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    total_weight = serializers.DecimalField(max_digits=15, decimal_places=2)

class SilverStockSummarySerializer(serializers.Serializer):
    warehouse = serializers.CharField()
    warehouse_code = serializers.CharField()
    total_products = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    total_weight = serializers.DecimalField(max_digits=15, decimal_places=2)