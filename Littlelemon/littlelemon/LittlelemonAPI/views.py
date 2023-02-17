from django.shortcuts import render, get_object_or_404
from .serializers import CategorySerializer,MenuItemSerializer,CartSerializer,OrderItemSerializer,OrderSerializer,UserSerializer
from .models import Order,OrderItem,MenuItem,Cart,Category
from rest_framework import generics , status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User, Group
from .permission import IsDeliveryCrew,IsManager
import datetime
# Create your views here.




class MenuItemsListView(generics.ListCreateAPIView):
 
    queryset = MenuItem.objects.all()
    serializer_class= MenuItemSerializer
    ordering_fields = ["title", "price"]
    def get_permissions(self):
        permission_class = [] # allow any user can retieve menuitem
        if self.request.user != 'GET':
            permission_class = [IsAdminUser|IsAuthenticated]
        return [permission() for permission in permission_class]


class SingleItemVIew(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuItem.objects.all()

    serializer_class=MenuItemSerializer

class ManagerView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name="manager")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser|IsManager&IsAuthenticated]


    def post(self,request,*agrs,**kwagrs):
        username = request.data['username']
        if username == request.POST['username']:
            user = get_object_or_404(User,username=username)
            manager= Group.objects.get(name='manager')
            
            try:
                if request.method == 'POST':
                    manager.user_set.add(user)
                    return Response(data={'message': 'Sucessfully add user to manager group'}, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response(data={'message':'You are not belong to manager group.'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'message': 'somthing went wrong'}, status= status.HTTP_400_BAD_REQUEST)
        
class ManagerDeleteView(generics.RetrieveDestroyAPIView):
        permission_classes= [IsAdminUser|IsManager&IsAuthenticated]
        queryset = User.objects.filter(groups__name="manager")
        serializer_class = UserSerializer
        def delete(self,request,pk=None):
            try:
                user= User.objects.get(pk=pk)    
                manager = Group.objects.get(name='manager')
                manager.user_set.remove(user)
                return Response(data={'message':f'You has been removed {user.username} from the group'},status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response(data={'message':f'There is no {user.username} from the data'},status=status.HTTP_404_NOT_FOUND )


class DeleiveryCrewListView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name="delivery_crew")
    serializer_class = UserSerializer
    permission_classes = [IsManager|IsDeliveryCrew&IsAuthenticated]

    def post(self,request,*agrs,**kwagrs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User,username=username)
            delivery_crew= Group.objects.get(name='delivery_crew')
          
            if request.method == 'POST':
                delivery_crew.user_set.add(user)
                return Response(data={'message': 'Sucessfully add user to delivery group'}, status=status.HTTP_201_CREATED)
            
        return Response(data={'message': 'somthing went wrong'}, status= status.HTTP_400_BAD_REQUEST)
class DeliveryCrewDeleteView(generics.RetrieveDestroyAPIView):
    permission_classes= [IsManager|IsDeliveryCrew&IsAuthenticated]
    queryset = User.objects.filter(groups__name="delivery_crew")
    serializer_class = UserSerializer
    def delete(self,request,pk=None):
        try:
            user= User.objects.get(pk=pk)    
            manager = Group.objects.get(name='delivery_crew')
            manager.user_set.remove(user)
            return Response(data={'message':f'You has been removed {user.username} from the delivery group'},status=status.HTTP_201_CREATED)
        except:
            
            return Response(data={'message':f'something went wrong the with user {user.username}'},status=status.HTTP_404_NOT_FOUND )
        


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
 
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    #get all items of current authenticate user
    def get_queryset(self):
        user= self.request.user
        return Cart.objects.select_related('menuitem').filter(user=user)

    def post(self, request, pk=None):
       
       
            user = self.request.user
            menuitem = MenuItem.objects.get(pk=self.request.data['menuitem'])
            quantity= int(self.request.data['quantity'])
            unit_price = menuitem.price
            price = quantity * unit_price

            new_cart = Cart(user=user,menuitem=menuitem,quantity=quantity,unit_price=unit_price,price=price)
            new_cart.save()
        
            return Response(data=CartSerializer(new_cart).data,status=status.HTTP_200_OK)
       
    def delete(self,request):
        cart = Cart.objects.filter(user=self.request.user)
        cart.delete()
        return Response(data={'message': f'There is no item in {self.request.user.username} Cart'},status=status.HTTP_200_OK)
    
class OrderListView(generics.ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    ordering_fields = ["user", "status", "total"]
    def get_queryset(self):
        
        user = self.request.user    
        if user.groups.filter(name='manager').exists():
            return Order.objects.all()
        if user.groups.filter(name='delivery_crew').exists():
            return Order.objects.all().filter(delivery_crew=user)
        
        return Order.objects.all().filter(user=user)

    def post(self, request, *args, **kwargs):
        user= self.request.user
        if  user.groups.filter(name='customer').exists():
            cart = Cart.objects.all().select_related('menuitem').filter(user=user)
            if not cart:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)
            total = 0
            for item in cart:
                total += item.price

            order= Order(user=self.request.user,total=total,date= datetime.datetime.now())
            order.save()
            for item in cart:
                orderitem=OrderItem(order=order,menuitem=item.menuitem,quantity=item.quantity,unit_price=item.unit_price,price=item.price)
                orderitem.save()
            cart.delete()
            return Response(data={'message':'Your order has been placed'},status=status.HTTP_201_CREATED)
        
        return Response({'message':'something went wrong'},status=status.HTTP_204_NO_CONTENT)
    
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
  
    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='manager').exists():
            return Order.objects.all()
        if user.groups.filter(name='delivery_crew').exists():
            return Order.objects.all()
        return Order.objects.all().filter(user=user)

     
    def get_permissions(self):
        permission_class = []
        if self.request.method in [ 'PUT','PATCH', 'DELETE']:
                permission_class = [IsManager]

        return [permission() for permission in permission_class]