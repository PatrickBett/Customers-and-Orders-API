import pytest
from customers.models import Customer, Order
from django.utils import timezone

@pytest.mark.django_db
def test_customer_str():
    customer = Customer.objects.create(
        name = "Patrick",
        code = "CUST1",
        phone_number = "+254791474737"
        )
    assert str(customer) == "Patrick"


@pytest.mark.django_db
def test_order_str():
    customer = Customer.objects.create(
        name = "Patrick",
        code = "CUST1",
        phone_number = "+254791474737"
        )
    order = Order.objects.create(
        customer = customer,
        item="Shoes",
        amount = 2000.00,
        order_time = timezone.now()
    )
    assert str(order) == "Shoes - Patrick"

