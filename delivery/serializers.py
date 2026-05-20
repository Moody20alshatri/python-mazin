# delivery/serializers.py
from rest_framework import serializers
from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    # هذا يضيف اسم العميل بدل رقمه فقط
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Delivery
        fields = ['id', 'customer', 'customer_name', 'delivery_address', 'amount', 'status', 'created_at']