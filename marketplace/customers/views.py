from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import CustomUser, Order
from .serializers import CustomerSerializer, OrderSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout

from django.shortcuts import redirect




class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # disables CSRF check
    
@api_view(['GET'])
def login_success(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Not authenticated"}, status=401)
    return redirect("https://customerorder.netlify.app/dashboard/")

# Using APIView
@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return Response({"message": "Customer Orders API"})


class CustomerListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customers = CustomUser.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Orders

class OrderListCreateAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Not authenticated"}, status=401)
        orders = Order.objects.filter(customer=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # can call SMS sending logic
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def current_user(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Not authenticated"}, status=401)
    
    # Return only the fields you want to expose to frontend
    return Response({
        "id": str(request.user.id),
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "profile_picture": request.user.profile_picture,
        "account_balance": float(request.user.account_balance),
        "code": request.user.code,
    })
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"detail": "Successfully logged out"}, status=200)

