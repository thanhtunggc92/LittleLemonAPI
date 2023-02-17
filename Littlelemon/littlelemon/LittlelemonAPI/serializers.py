from rest_framework import serializers 
from .models import MenuItem,Category,Cart,Order,OrderItem
from django.contrib.auth.models import User




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = '__all__'
class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only= True)
    # category_id = serializers.IntegerField(write_only = True)
    category = serializers.PrimaryKeyRelatedField(
        queryset= Category.objects.all()
    )
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user','menuitem','quantity','unit_price','price']

    


class OrderItemSerializer(serializers.ModelSerializer):
        class Meta: 
            model = OrderItem
          
            fields= ['order','menuitem','quantity','unit_price','price']
     
     
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']


class OrderSerializer(serializers.ModelSerializer):
    order_items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
     
        fields = ['user','delivery_crew','status','total','date','order_items']

        extra_kwargs = {
            "total": {"read_only": True},
            "date": {"read_only": True},
        }
    