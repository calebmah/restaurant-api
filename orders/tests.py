import json

from django.contrib.auth.models import User
from django.db.models import Avg, Sum
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from .models import MenuItems, Orders, Restaurants
from .serializers import OrderSerializer

# tests for views

class BaseViewTest(APITestCase):
    client = APIClient()

    def create_order(self, restaurant, quantity, item, user=None):
        if user:
            Orders.objects.create(restaurant=restaurant, quantity=quantity,item=item,user=user)
        else:
            Orders.objects.create(restaurant=restaurant, quantity=quantity,item=item,user=self.user)

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

        # mock test data
        self.valid_id = 1
        self.invalid_id = 1000
        self.valid_restaurant = "Burger"
        self.invalid_restaurant = "Not a restaurant"

        restaurant = Restaurants.objects.create(name=self.valid_restaurant)
        item_beef = MenuItems.objects.create(restaurant=restaurant,name="beef",price=2)
        item_chicken = MenuItems.objects.create(restaurant=restaurant,name="chicken",price=1.5)

        self.create_order(restaurant, 3, item_beef)
        self.create_order(restaurant, 6, item_chicken)

    def login_client(self, username="", password=""):
        # get a token from DRF API
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
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

class GetAllOrdersTest(BaseViewTest):

    def test_get_all_orders(self):
        """
        Test that GET orders/ endpoint returns all orders in db
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

class CreateOrderTest(BaseViewTest):

    def test_create_orders(self):
        """
        Test POST orders/ for the creation of a new order
        """
        # hit the API endpoint
        response = self.client.post(
            reverse("orders-all"),
            {
                "restaurant": "Burger",
                "quantity": 9,
                "item": "beef"
            }
        )
        # fetch the data from db
        expected = Orders.objects.get(pk=3)
        serialized = OrderSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class GetASingleOrdersTest(BaseViewTest):

    def test_get_order_by_order_id(self):
        """
        Test that GET orders/<int:pk>/ returns a single order of given id
        """
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
            response.data,
            {"detail": ErrorDetail(string='Not found.', code='not_found')}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GetListOfOrdersTest(BaseViewTest):
    def test_get_orders_by_customer_id(self):
        """
        Test that GET orders/customer/<int:customer>/ returns list of orders from customer id
        """
        # hit the API endpoint
        response = self.client.get(
            reverse(
                "orders-customer",
                kwargs={
                    "customer": self.valid_id
                }
            )
        )
        # fetch the data from db
        expected = Orders.objects.filter(user=self.valid_id)
        serialized = OrderSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a customer that does not exist
        response = self.client.get(
            reverse(
                "orders-customer",
                kwargs={
                    "customer": self.invalid_id
                }
            )
        )
        self.assertEqual(
            response.data["message"],
            f"Customer with id: {self.invalid_id} does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_orders_by_restaurant_id(self):
        """
        Test that GET orders/restaurant/<str:restaurant>/ returns list of orders from restaurant id
        """
        # hit the API endpoint
        response = self.client.get(
            reverse(
                "orders-restaurant",
                kwargs={
                    "restaurant": self.valid_restaurant
                }
            )
        )
        # fetch the data from db
        expected = Orders.objects.filter(restaurant=self.valid_restaurant)
        serialized = OrderSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a restaurant that does not exist
        response = self.client.get(
            reverse(
                "orders-restaurant",
                kwargs={
                    "restaurant": self.invalid_restaurant
                }
            )
        )
        self.assertEqual(
            response.data["message"],
            f"Restaurant with name: {self.invalid_restaurant} does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GetCostTest(BaseViewTest):
    def test_get_cost_by_restaurant_id(self):
        """
        Test that GET orders/cost/<str:restaurant> returns list of orders from customer id
        """
        # hit the API endpoint
        response = self.client.get(
            reverse(
                "cost-single",
                kwargs={
                    "restaurant": self.valid_restaurant
                }
            )
        )
        # fetch the data from db
        expected = Orders.objects.filter(restaurant=self.valid_restaurant).aggregate(Sum('total_price')).get("total_price__sum")
        self.assertEqual(response.data.get('cost',''), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a restaurant that does not exist
        response = self.client.get(
            reverse(
                "cost-single",
                kwargs={
                    "restaurant": self.invalid_restaurant
                }
            )
        )
        self.assertEqual(
            response.data["message"],
            f"Restaurant with name: {self.invalid_restaurant} does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GetAveQuantityTest(BaseViewTest):
    def test_get_average_quantity_by_restaurant_id(self):
        """
        Test that GET orders/stats/average-quantity/<str:restaurant> returns average quantity from restaurant id
        """
        # hit the API endpoint
        response = self.client.get(
            reverse(
                "average-quantity",
                kwargs={
                    "restaurant": self.valid_restaurant,
                    "customer": self.valid_id
                }
            )
        )
        # fetch the data from db
        expected = Orders.objects.filter(restaurant=self.valid_restaurant).aggregate(Avg('quantity')).get("quantity__avg")
        self.assertEqual(response.data.get('average',''), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a restaurant that does not exist
        response = self.client.get(
            reverse(
                "average-quantity",
                kwargs={
                    "restaurant": self.invalid_restaurant,
                    "customer": self.valid_id
                }
            )
        )
        self.assertEqual(
            response.data["message"],
            f"Restaurant with name: {self.invalid_restaurant} does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # test with a customer that does not exist
        response = self.client.get(
            reverse(
                "average-quantity",
                kwargs={
                    "restaurant": self.valid_restaurant,
                    "customer": self.invalid_id
                }
            )
        )
        self.assertEqual(
            response.data["message"],
            f"Customer with id: {self.invalid_id} does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
