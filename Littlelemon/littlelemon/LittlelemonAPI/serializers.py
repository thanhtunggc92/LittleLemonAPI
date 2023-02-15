from rest_framework import serializers 
from .models import MenuItem,Category,Cart,Order,OrderItem





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = '__all__'
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only= True)
    category_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category','category_id']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user','menuitem','quantity','unit_price','price']


class OrderSerializer(serializers.ModelField):
    class Meta:
        model = Order
        fields = ['user','delivery_crew','status','total','date']

    def total_price(self,product:OrderItem):
        return product.quantity * product.unit_price
