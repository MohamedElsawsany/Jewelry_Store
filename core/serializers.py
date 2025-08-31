from rest_framework import serializers
from .models import Branch, Warehouse, Vendor, Customer, Seller, WarehouseTransaction

class BranchSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'created_date', 'updated_date', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'updated_date', 'created_by_username']

class WarehouseSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Warehouse
        fields = ['id', 'code', 'branch', 'branch_name', 'cash', 'created_date', 
                 'updated_date', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'updated_date', 'created_by_username']

class VendorSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'created_date', 'updated_date', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'updated_date', 'created_by_username']

class CustomerSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'created_date', 'updated_date', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'updated_date', 'created_by_username']

class SellerSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Seller
        fields = ['id', 'name', 'branch', 'branch_name', 'created_date', 
                 'updated_date', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'updated_date', 'created_by_username']

class WarehouseTransactionSerializer(serializers.ModelSerializer):
    from_warehouse_code = serializers.CharField(source='from_warehouse.code', read_only=True)
    to_warehouse_code = serializers.CharField(source='to_warehouse.code', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    action_by_username = serializers.CharField(source='action_by.username', read_only=True)
    
    class Meta:
        model = WarehouseTransaction
        fields = ['id', 'item_name', 'from_warehouse', 'from_warehouse_code', 
                 'to_warehouse', 'to_warehouse_code', 'quantity', 'status', 
                 'action_by', 'action_by_username', 'action_date', 'created_date', 
                 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_date', 'created_by_username', 'action_by_username']

    def validate(self, data):
        if data['from_warehouse'] == data['to_warehouse']:
            raise serializers.ValidationError("From and to warehouses must be different")
        return data