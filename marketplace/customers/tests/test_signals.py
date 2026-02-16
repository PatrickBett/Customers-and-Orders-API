import pytest
from customers.models import CustomUser, Order, OrderItem
from unittest.mock import patch

@pytest.mark.django_db
@patch("customers.signals.send_sms")  # Ensure this path matches where you import send_sms
def test_order_creation_triggers_sms(mock_send_sms):
    # 1. Setup Customer
    customer = CustomUser.objects.create_user(
        username="Alice",
        code="CUST2",
    )
    
    # 2. Create Order 
    # This triggers the 'post_save' signal
    order = Order.objects.create(
        customer=customer,
        phone_number="+254712345670",
        total_price=1500.00
    )

    # 3. Assert SMS utility was called
    assert mock_send_sms.called
    mock_send_sms.assert_called_once()
    
    # 4. Check the arguments passed to send_sms
    args, _ = mock_send_sms.call_args
    # args[0] is phone_number, args[1] is the message
    assert args[0] == "+254712345670"
    assert "Alice" in args[1]
    assert "1500.0" in args[1]