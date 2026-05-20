# customers/admin.py
from django.contrib import admin
from .models import Customer

# ليش؟ عشان تظهر في لوحة التحكم وتقدر تضيف وتعدل وتحذف
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # الأعمدة اللي تظهر في القائمة
    list_display = ['id', 'name', 'phone', 'address', 'created_at']
    # بحث
    search_fields = ['name', 'phone']