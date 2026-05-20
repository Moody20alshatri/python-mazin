# delivery/admin.py
from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'amount', 'created_at']
    search_fields = ['customer__name']
    # فلتر بالحالة
    list_filter = ['status']