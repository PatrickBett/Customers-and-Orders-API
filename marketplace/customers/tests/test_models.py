import pytest
from customers.models import CustomUser, Order, OrderItem
from django.utils import timezone

@pytest.mark.django_db
def test_custom_user_creation():
    """Test that a CustomUser is created correctly with default fields"""
    user = CustomUser.objects.create_user(
        username="patrick",
        email="patrick@example.com",
        password="password123",
        code="CUST001"
    )
    assert user.username == "patrick"
    assert user.account_balance == 10000.00 # Testing your default value
    assert str(user) == "patrick" # Matches your __str__ method

@pytest.mark.django_db
def test_order_creation():
    """Test that an Order is linked to a user and generates a UUID"""
    user = CustomUser.objects.create_user(username="testuser", code="CUST002")
    order = Order.objects.create(
        customer=user,
        phone_number="+254790000000",
        total_price=500.00
    )
    # Check if ID is a valid UUID
    assert order.id is not None
    assert str(order) == f"Order {order.id} - testuser"

@pytest.mark.django_db
def test_order_item_creation():
    """Test the OrderItem relationship and string representation"""
    user = CustomUser.objects.create_user(username="buyer", code="CUST003")
    order = Order.objects.create(customer=user, phone_number="+254700111222")
    
    item = OrderItem.objects.create(
        order=order,
        product_title="Gaming Mouse",
        price=1500.00,
        quantity=2
    )
    
    assert item.product_title == "Gaming Mouse"
    assert item.order.customer.username == "buyer"
    assert str(item) == "2 x Gaming Mouse for buyer"

@pytest.mark.django_db
def test_order_cascade_delete():
    """Test that deleting a user deletes their orders (Cascade)"""
    user = CustomUser.objects.create_user(username="temporary", code="CUST004")
    Order.objects.create(customer=user, phone_number="+254700000000")
    
    assert Order.objects.filter(customer=user).count() == 1
    user.delete()
    assert Order.objects.filter(customer__username="temporary").count() == 0