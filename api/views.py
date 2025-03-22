from django.db.models import Max
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from .models import Product, Order, OrderItem
from .filters import ProductFilter
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
 
 
class ProductCreateList(generics.ListCreateAPIView) :
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "descriptions"]
    ordering_fields = ["name", "price", "stock"]
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST" :
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductDetail(generics.RetrieveUpdateDestroyAPIView) :
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"] :
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class OrderList(generics.ListAPIView) :
    queryset = Order.objects.all().prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user= user)

class ProductInfo(APIView) :
    def get(self, request) :
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {"products" : products,
            "count" : len(products),
            "max_price": products.aggregate(max_price= Max('price'))["max_price"]
            }
        )
        return Response(serializer.data) 



