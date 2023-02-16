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

    
class OrderSerializer(serializers.ModelField):
    class Meta:
        model = Order
     
        fields = ['user','delivery_crew','status','total','date']

    def total_price(self,product:OrderItem):

        total += product.price
        return f'{total}'

class OrderItemSerializer(serializers.ModelSerializer):
        class Meta: 
            model = OrderItem
          
            fields= ['order','menuitem','quantity','unit_price','price']
     
     
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']
    