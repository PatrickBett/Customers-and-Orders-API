
from django.contrib import admin
from django.urls import path, include
from customers.views import home
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response

schema_view = get_schema_view(
   openapi.Info(
      title="Logistics Management API",
      default_version='v1',
      description="API for managing logistics operations",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('oidc/', include('mozilla_django_oidc.urls')),  # login, callback, logout
    path('admin/', admin.site.urls),
    path('api/', include('customers.urls')),
    path('',home, name='home')
]
