import pytest
from customers.models import Customer, Order
from unittest.mock import patch

@pytest.mark.django_db
@patch("customers.signals.send_sms")
def test_order_creation_triggers_sms(mock_send_sms):
    customer = Customer.objects.create(
        name ="Alice",
        code = "CUST2",
        phone_number = "+254712345670"
        )
    order = Order.objects.create(
        customer = customer,
        item = "Laptop",
        amount = 1500.00
    )

    #Assert SMS was called
    mock_send_sms.assert_called_once()
    args, kwargs = mock_send_sms.call_args
    assert args[0] == "+254712345670"
    assert "Laptop" in args[1]