from django.db import models
from utils.mixins import TimestampedModel, CreatedByModel

class GoldInvoice(TimestampedModel, CreatedByModel):  # No soft delete
    TRANSACTION_CHOICES = [
        ('Cash', 'Cash'),
        ('Visa', 'Visa'),
    ]
    
    INVOICE_TYPE_CHOICES = [
        ('Sale', 'Sale'),
        ('Return Packing', 'Return Packing'),
        ('Return Unpacking', 'Return Unpacking'),
    ]
    
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='gold_invoices')
    seller = models.ForeignKey('core.Seller', on_delete=models.CASCADE, related_name='gold_invoices')
    branch = models.ForeignKey('core.Branch', on_delete=models.CASCADE, related_name='gold_invoices')
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE, related_name='gold_invoices')
    gold_price_21 = models.DecimalField(max_digits=10, decimal_places=2)
    gold_price_24 = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_CHOICES, default='Cash')
    invoice_type = models.CharField(max_length=255, choices=INVOICE_TYPE_CHOICES)
    
    class Meta:
        db_table = 'gold_invoice'
    
    def __str__(self):
        return f"Gold Invoice #{self.id} - {self.customer.name} - {self.total_price}"

class GoldInvoiceItem(models.Model):  # No soft delete and no timestamps (matches original schema)
    invoice = models.ForeignKey(GoldInvoice, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    item_weight = models.DecimalField(max_digits=10, decimal_places=2)
    item_carat = models.DecimalField(max_digits=10, decimal_places=2)
    item_stamp_enduser = models.DecimalField(max_digits=10, decimal_places=2)
    item_quantity = models.BigIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'gold_invoice_items'
    
    def __str__(self):
        return f"{self.item_name} - Qty: {self.item_quantity}"

class SilverInvoice(TimestampedModel, CreatedByModel):  # No soft delete
    TRANSACTION_CHOICES = [
        ('Cash', 'Cash'),
        ('Visa', 'Visa'),
    ]
    
    INVOICE_TYPE_CHOICES = [
        ('Sale', 'Sale'),
        ('Return Packing', 'Return Packing'),
        ('Return Unpacking', 'Return Unpacking'),
    ]
    
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='silver_invoices')
    seller = models.ForeignKey('core.Seller', on_delete=models.CASCADE, related_name='silver_invoices')
    branch = models.ForeignKey('core.Branch', on_delete=models.CASCADE, related_name='silver_invoices')
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE, related_name='silver_invoices')
    silver_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_CHOICES, default='Cash')
    invoice_type = models.CharField(max_length=255, choices=INVOICE_TYPE_CHOICES)
    
    class Meta:
        db_table = 'silver_invoice'
    
    def __str__(self):
        return f"Silver Invoice #{self.id} - {self.customer.name} - {self.total_price}"

class SilverInvoiceItem(models.Model):  # No soft delete and no timestamps
    invoice = models.ForeignKey(SilverInvoice, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    item_weight = models.DecimalField(max_digits=10, decimal_places=2)
    item_carat = models.DecimalField(max_digits=10, decimal_places=2)
    item_stamp_enduser = models.DecimalField(max_digits=10, decimal_places=2)
    item_quantity = models.BigIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'silver_invoice_items'
    
    def __str__(self):
        return f"{self.item_name} - Qty: {self.item_quantity}"