from django.test import TestCase
from .models import User, Order
from django.urls import reverse
from rest_framework import status
class UserOrderTest(TestCase) :
    def setUp(self):
        user1 = User.objects.create_user(username= "test1", password= "pass")
        user2 = User.objects.create_user(username= "test2", password= "pass")
        Order.objects.create(user = user1)
        Order.objects.create(user = user2)
    
    def test_user_order_endpoint_retrieves_only_authenticated_user_order(self) :
        user = User.objects.get(username= "test1")
        self.client.force_login(user= user)
        response = self.client.get(reverse("api:order-list"))
         
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_user_orders_list_unauthenticated(self) :
        response = self.client.get(reverse("api:order-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
 
