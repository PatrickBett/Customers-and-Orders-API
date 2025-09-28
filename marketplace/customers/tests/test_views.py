import pytest
from rest_framework.test import APIClient
from customers.models import Customer
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_get_customers_list():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="pass123")
    client.force_authenticate(user=user)

    Customer.objects.create(name="Bob", code="CUST3", phone_number="+254700000333")

    response = client.get("/api/customers/")
    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.django_db
def test_create_order_triggers_sms(mocker):
    client = APIClient()
    user = User.objects.create_user(username="testuser2", password="pass123")
    client.force_authenticate(user=user)

    customer = Customer.objects.create(name="Carol", code="C127", phone_number="+254700000444")

    # Mock SMS
    mocker.patch("customers.signals.send_sms")

    response = client.post("/api/orders/", {
        "customer": str(customer.id),
        "item": "Phone",
        "amount": "1200.00"
    }, format="json")

    assert response.status_code == 201

@pytest.mark.django_db
def test_home_view():
    client = APIClient()
    response = client.get("/")   # adjust path if you mounted home under a different url
    assert response.status_code == 200
    assert response.json() == {"message": "Customer Orders API"}

@pytest.mark.django_db
def test_create_customer_invalid():
    client = APIClient()
    # Create a dummy user
    user = User.objects.create_user(username="tester", password="pass123")
    client.force_authenticate(user=user)
    # Missing "name" which is required
    data = {
        "code": "CUST123",
        "phone_number": "1234567890"
    }
    response = client.post("/api/customers/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.json()

@pytest.fixture
def auth_client(db):
    client = APIClient()
    user = User.objects.create_user(username="tester", password="pass123")
    client.force_authenticate(user=user)
    return client


# --- Order invalid: missing customer ---
@pytest.mark.django_db
def test_create_order_invalid_missing_customer(auth_client):
    response = auth_client.post("/api/orders/", {
        "item": "Laptop",
        "amount": "1200.00"
    }, format="json")
    assert response.status_code == 400
    assert "customer" in response.json()


# --- Customer invalid ---
@pytest.mark.django_db
def test_create_customer_invalid_missing_code(auth_client):
    response = auth_client.post("/api/customers/", {
        "name": "No Code",
        "phone_number": "+254700000111"
    }, format="json")

@pytest.mark.django_db
def test_create_order_invalid_missing_item(auth_client):
    customer = Customer.objects.create(
        name="John",
        code="CUSTX",
        phone_number="+254700000222"
    )
    response = auth_client.post("/api/orders/", {
        "customer": str(customer.id),
        "amount": "500.00"
    }, format="json")
