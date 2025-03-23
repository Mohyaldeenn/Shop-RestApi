from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = "api"

urlpatterns = [
    path("products/", views.ProductCreateList.as_view(), name= "product-list" ),
    path("product_info/", views.ProductInfo.as_view(), name= "product-info" ),
    path("products/<int:pk>", views.ProductDetail.as_view(), name= "product-detail" ),
    # path("orders/", views.OrderList.as_view(), name= "order-list" ),
]

router = DefaultRouter()
router.register("orders", views.OrderViewSet)
urlpatterns += router.urls
