from rest_framework.test import APITestCase
from .models import User, Order, Product
from django.urls import reverse
from rest_framework import status


class ProductApiTestCase(APITestCase) :
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username= "admin", password= "pass")
        self.user = User.objects.create_user(username= "user", password= "pass")
        self.product = Product.objects.create(
            name = "test product", descriptions = "test description", price= 11.34, stock = 10
        )
        self.url = reverse("api:product-detail", kwargs= {"pk" : self.product.pk})
        
    def test_get_product(self) :
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)
    
    def test_unauthorized_update_product(self) :
        data = {"name" : "update test"}
        response = self.client.put(self.url, data)    
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
      
    def test_only_admin_can_delete_product(self) :
        self.client.login(username = "user", password= "pass" )
        response = self.client.delete(self.url)    
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  
        self.assertTrue(Product.objects.filter(pk= self.product.pk).exists())

        self.client.login(username = "admin", password= "pass" )
        response = self.client.delete(self.url)    
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  
        self.assertFalse(Product.objects.filter(pk= self.product.pk).exists())