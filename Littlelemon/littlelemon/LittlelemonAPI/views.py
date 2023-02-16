from django.shortcuts import render, get_object_or_404
from .serializers import CategorySerializer,MenuItemSerializer,CartSerializer,OrderItemSerializer,OrderSerializer,UserSerializer
from .models import Order,OrderItem,MenuItem,Cart,Category
from rest_framework import generics , status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User, Group
from .permission import IsDeliveryCrew,IsManager
# Create your views here.




class MenuItemsListView(generics.ListCreateAPIView):
 
    queryset = MenuItem.objects.all()
    serializer_class= MenuItemSerializer

    def get_permissions(self):
        permission_class = [] # allow any user can retieve menuitem
        if self.request.user != 'GET':
            permission_class = [IsAdminUser|IsAuthenticated]
        return [permission() for permission in permission_class]


class SingleItemVIew(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuItem.objects.all()

    serializer_class=MenuItemSerializer

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class ManagerView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name="manager")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser|IsManager]
    # def get(self,request, *agrs,**kwagrs):
    #     username= request.data['username']
    #     if request.metho =='GET':
    #         manager= UserSerializer

    def post(self,request,*agrs,**kwagrs):
        username = request.data['username']

        if username:

            user = get_object_or_404(User,username=username)
            manager= Group.objects.get(name='manager')
            if manager == 'manager':
                if request.method == 'POST':
                    manager.user_set.add(user)
                    return Response(data={'message': 'Sucessfully add user to manager group'}, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'message':'You are not belong to manager group.'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'message': 'somthing went wrong'}, status= status.HTTP_400_BAD_REQUEST)
        
class ManagerDeleteView(generics.RetrieveDestroyAPIView):
    pass

#  if request.method == 'DELETE':
#     manager.user_set.remove(user)
#     return Response(data={'message': 'Sucessfully add delete to manager group'}, status=status.HTTP_201_CREATED)