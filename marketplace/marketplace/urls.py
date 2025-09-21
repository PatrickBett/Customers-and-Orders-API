
from django.contrib import admin
from django.urls import path, include
from customers.views import home
urlpatterns = [
    path('oidc/', include('mozilla_django_oidc.urls')),  # login, callback, logout
    path('admin/', admin.site.urls),
    path('api/', include('customers.urls')),
    path('',home, name='home')
]
