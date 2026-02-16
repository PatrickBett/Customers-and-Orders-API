import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    code = models.CharField(max_length=50, unique=True) 
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    profile_picture = models.URLField(max_length=1024,blank=True, null=True)
    def __str__(self):
        return self.username

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"

class OrderItem(models.Model):
    # 'related_name' allows you to do order.items_in_order.all()
    order = models.ForeignKey(Order, related_name='items_in_order', on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_title} for {self.order.customer.username}"