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
    order_id = serializers.UUIDField(read_only= True)
    items = OrderItemSerializer(many= True, read_only= True)
    total_price = serializers.SerializerMethodField()
    def get_total_price(self, obj) :
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta :
        model = Order
        fields = ("order_id", "created_at", "user", "status", "items", "total_price",)


class OrderCreateSerializer(serializers.ModelSerializer) :
    class OrderItemCreateSerializer(serializers.ModelSerializer) :
        class Meta :
            model = OrderItem
            fields = ("product", "quantity")
    
    items = OrderItemCreateSerializer(many= True)
    
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order=  Order.objects.create(**validated_data)
        for item in items_data :
            OrderItem.objects.create(order= order, **item)
        return order
        
    class Meta :
        model = Order
        fields = ("user", "status", "items")
        extra_kwargs = {
           "user" : {"read_only" : True} 
        }
class ProductInfoSerializer(serializers.Serializer) :
    products = ProductSerializer(many= True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()