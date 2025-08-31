from django.db import models
from utils.mixins import SoftDeleteModel, TimestampedModel, CreatedByModel

class Branch(SoftDeleteModel, TimestampedModel, CreatedByModel):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'branches'
        verbose_name_plural = 'Branches'
    
    def __str__(self):
        return self.name

class Warehouse(SoftDeleteModel, TimestampedModel, CreatedByModel):
    code = models.CharField(max_length=255, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='warehouses')
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'warehouse'
    
    def __str__(self):
        return f"{self.code} - {self.branch.name}"

class Vendor(SoftDeleteModel, TimestampedModel, CreatedByModel):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'vendors'
    
    def __str__(self):
        return self.name

class Customer(SoftDeleteModel, TimestampedModel, CreatedByModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return f"{self.name} - {self.phone}"

class Seller(SoftDeleteModel, TimestampedModel, CreatedByModel):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='sellers')
    
    class Meta:
        db_table = 'sellers'
    
    def __str__(self):
        return f"{self.name} - {self.branch.name}"

class WarehouseTransaction(TimestampedModel, CreatedByModel):  # No soft delete
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    item_name = models.CharField(max_length=255)
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='outgoing_transactions')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='incoming_transactions')
    quantity = models.BigIntegerField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    action_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='warehouse_actions')
    action_date = models.DateTimeField()
    
    class Meta:
        db_table = 'warehouse_transactions'
    
    def __str__(self):
        return f"{self.item_name} - {self.from_warehouse.code} to {self.to_warehouse.code}"