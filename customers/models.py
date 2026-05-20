# customers/models.py
from django.db import models


class Customer(models.Model):
    

    name = models.CharField(max_length=100)
    

    phone = models.CharField(max_length=15)

    address = models.TextField()
    
  
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
  
        db_table = 'customers'