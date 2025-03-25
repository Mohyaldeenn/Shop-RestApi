from django.db.models import Max
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer, OrderCreateSerializer
from .models import Product, Order, OrderItem
from .filters import ProductFilter, OrderFilter
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
 
 
class ProductCreateList(generics.ListCreateAPIView) :
    queryset = Product.objects.all().order_by("pk")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "descriptions"]
    ordering_fields = ["name", "price", "stock"]
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6
    pagination_class.max_page_size = 11 
    
    @method_decorator(cache_page(60 * 15, key_prefix= "product_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
    
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


class OrderViewSet(viewsets.ModelViewSet) :
    queryset = Order.objects.all().prefetch_related("items__product").order_by("pk")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        qs = self.queryset
        if not self.request.user.is_staff :
            qs = qs.filter(user= self.request.user) 
        return qs
    
    def get_serializer_class(self):
        if self.action == "create" or self.action == "update"  :
            return OrderCreateSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        serializer.save(user= self.request.user)
    
    
# class OrderList(generics.ListAPIView) :
#     queryset = Order.objects.all().prefetch_related("items__product")
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         user = self.request.user
#         qs = super().get_queryset()
#         return qs.filter(user= user)

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



