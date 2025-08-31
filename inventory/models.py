from django.db import models
from utils.mixins import SoftDeleteModel, TimestampedModel, CreatedByModel

class GoldProduct(SoftDeleteModel, TimestampedModel, CreatedByModel):
    vendor = models.ForeignKey('core.Vendor', on_delete=models.CASCADE, related_name='gold_products')
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    carat = models.DecimalField(max_digits=10, decimal_places=2)
    stamp_enduser = models.DecimalField(max_digits=10, decimal_places=2)
    cashback = models.DecimalField(max_digits=10, decimal_places=2)
    cashback_unpacking = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'gold_products'
    
    def __str__(self):
        return f"{self.name} - {self.weight}g - {self.carat}K"

class SilverProduct(SoftDeleteModel, TimestampedModel, CreatedByModel):
    vendor = models.ForeignKey('core.Vendor', on_delete=models.CASCADE, related_name='silver_products')
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    carat = models.DecimalField(max_digits=10, decimal_places=2)
    stamp_enduser = models.DecimalField(max_digits=10, decimal_places=2)
    cashback = models.DecimalField(max_digits=10, decimal_places=2)
    cashback_unpacking = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'silver_products'
    
    def __str__(self):
        return f"{self.name} - {self.weight}g - {self.carat}K"

class GoldWarehouseStock(SoftDeleteModel, TimestampedModel, CreatedByModel):
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='gold_stock')
    product = models.ForeignKey(GoldProduct, on_delete=models.CASCADE, related_name='warehouse_stock')
    quantity = models.BigIntegerField(default=0)
    
    class Meta:
        db_table = 'gold_warehouse_stock'
        unique_together = ['warehouse', 'product']
    
    def __str__(self):
        return f"{self.product.name} - {self.warehouse.code} - Qty: {self.quantity}"

class SilverWarehouseStock(SoftDeleteModel, TimestampedModel, CreatedByModel):
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='silver_stock')
    product = models.ForeignKey(SilverProduct, on_delete=models.CASCADE, related_name='warehouse_stock')
    quantity = models.BigIntegerField(default=0)
    
    class Meta:
        db_table = 'silver_warehouse_stock'
        unique_together = ['warehouse', 'product']
    
    def __str__(self):
        return f"{self.product.name} - {self.warehouse.code} - Qty: {self.quantity}"