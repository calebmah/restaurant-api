import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from .models import MenuItems, Orders, Restaurants
from .serializers import OrderSerializer

# tests for views

class BaseViewTest(APITestCase):
    client = APIClient()

    def create_order(self, restaurant="", quantity="", item=""):
        if restaurant and quantity and item:
            Orders.objects.create(restaurant=restaurant, quantity=quantity,item=item)

    def setUp(self):
        # mock test user
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="test_pass",
            first_name="test",
            last_name="user",
        )
        self.login_client(username="test_user",password="test_pass")
        # add test data
        restaurant = Restaurants.objects.create(name="Burger")
        item_beef = MenuItems.objects.create(restaurant=restaurant,name="beef",price=2)
        item_chicken = MenuItems.objects.create(restaurant=restaurant,name="chicken",price=1.5)

        self.create_order(restaurant, 6, item_beef)
        self.create_order(restaurant, 6, item_chicken)

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('generate-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

class GetAllOrdersTest(BaseViewTest):

    def test_get_all_orders(self):
        """
        Test that order endpoint returns all orders in db
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("orders-all")
        )
        # fetch the data from db
        expected = Orders.objects.all()
        serialized = OrderSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetASingleOrdersTest(BaseViewTest):

    def test_get_a_order(self):
        """
        Test that order endpoint returns single order of given id
        """
        self.valid_id = 1
        self.invalid_id = 1000
        # hit the API endpoint
        response = self.client.get(
            reverse(
                "orders-single",
                kwargs={
                    "pk": self.valid_id
                }
            )
        )
        # fetch the data from db
        expected = Orders.objects.get(pk=self.valid_id)
        serialized = OrderSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with an order that does not exist
        response = self.client.get(
            reverse(
                "orders-single",
                kwargs={
                    "pk": self.invalid_id
                }
            )
        )
        self.assertEqual(
            response.data["message"],
            "Order with id: 1000 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
