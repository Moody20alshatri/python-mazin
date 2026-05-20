# delivery/models.py
from django.db import models
from customers.models import Customer


class Delivery(models.Model):

    # حالات التوصيل
    STATUS_CHOICES = [
        ('pending',     'قيد الانتظار'),
        ('in_progress', 'جاري التوصيل'),
        ('delivered',   'تم التوصيل'),
        ('cancelled',   'ملغي'),
    ]

    # العميل - مرتبط بجدول العملاء
    # on_delete=CASCADE يعني لو حذفنا العميل تحذف طلباته معه
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='deliveries'
    )

    delivery_address = models.TextField()

    
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery #{self.id} - {self.customer.name}"

    class Meta:
        db_table = 'deliveries'
        # رتّب من الأحدث للأقدم
        ordering = ['-created_at']