from django.urls import path
from .views import CustomerListCreateAPIView, OrderListCreateAPIView, current_user, login_success,logout_view

urlpatterns = [
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path("current_user/", current_user, name="current_user"),
    path("login-success/", login_success, name="login-success"),
    path("logout/", logout_view, name="api_logout"),
]
