from django.contrib import admin
from .models import CustomUser, Order, OrderItem
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(OrderItem)