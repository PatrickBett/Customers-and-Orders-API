from rest_framework import serializers
from django.db import transaction
from .models import  CustomUser, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_title', 'price', 'quantity']

# class OrderSerializer(serializers.ModelSerializer):
#     # This 'items' field matches the key name in your React payload
#     items = OrderItemSerializer(many=True, source='items_in_order')

#     class Meta:
#         model = Order.objects.none().model # Reference to Order
#         model = Order
#         fields = ['id', 'customer', 'phone_number', 'total_price', 'order_time', 'items']
#         read_only_fields = ['id', 'order_time']

#     def create(self, validated_data):
#         # 1. Pull the nested items out of the validated data
#         items_data = validated_data.pop('items_in_order')
        
#         # 2. Create the Order object first
#         order = Order.objects.create(**validated_data)
        
#         # 3. Create each OrderItem linked to this order
#         for item_data in items_data:
#             OrderItem.objects.create(order=order, **item_data)
            
#         return order
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='items_in_order')

    class Meta:
        model = Order
        fields = ['id', 'customer', 'phone_number', 'total_price', 'order_time', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items_in_order')
        customer = validated_data['customer']
        total_price = validated_data['total_price']

        # Wrap in a transaction so if anything fails, nothing is saved
        with transaction.atomic():
            # 1. Deduct the balance
            if customer.account_balance < total_price:
                raise serializers.ValidationError({"error": "Insufficient funds in database."})
            
            customer.account_balance -= total_price
            customer.save()

            # 2. Create the Order
            order = Order.objects.create(**validated_data)

            # 3. Create the Order Items
            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)

        return order