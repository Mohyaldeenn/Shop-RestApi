from rest_framework import serializers
from .models import Order, OrderItem, Product

class ProductSerializer(serializers.ModelSerializer) :
    
    class Meta :
        model = Product
        fields = ("name", "descriptions", "price", "stock")
        
    def validate_price(self, value ) :
        if value > 0 :
            return value
        else:
            raise  serializers.ValueError("price must be greater than 0")
        

class OrderItemSerializer(serializers.ModelSerializer) :
    product_name = serializers.CharField(source= "product.name")
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, source= "product.price" )
    class Meta :
        model = OrderItem
        fields = ("product_name", "product_price" , "quantity", "item_subtotal")
        

class OrderSerializer(serializers.ModelSerializer) :
    items = OrderItemSerializer(many= True, read_only= True)
    total_price = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    def get_total_price(self, obj) :
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta :
        model = Order
        fields = ("order_id", "created_at", "user", "status", "items", "total_price",)
        

class ProductInfoSerializer(serializers.Serializer) :
    products = ProductSerializer(many= True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()