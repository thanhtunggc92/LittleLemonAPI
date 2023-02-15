from django.shortcuts import render, get_object_or_404
from .serializers import CategorySerializer,MenuItemSerializer
from .models import Order,OrderItem,MenuItem,Cart,Category
from rest_framework import generics , status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.




class MenuItemView(generics.ListCreateAPIView):
 
    queryset = MenuItem.objects.all()
    serializer_class= MenuItemSerializer

class SingleItemVIew(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    