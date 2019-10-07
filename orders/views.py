from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import MenuItems, Orders, Restaurants
from .serializers import OrderSerializer


class OrdersListCreateView(generics.ListCreateAPIView):
    """
    GET orders/
    POST orders/
    """
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        restaurant=request.data.get("restaurant","")
        quantity=request.data.get("quantity","")
        item=request.data.get("item","")
        comments=request.data.get("comments","")

        if not restaurant or not quantity or not item:
            return Response(
                data={
                    "message": "restaurant, quantity and item are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            restaurant = Restaurants.objects.get(name=restaurant)
            item = MenuItems.objects.get(name=item)
            quantity = int(quantity)
        except ObjectDoesNotExist:
            return Response(
                    data={
                        "message": "restaurant or item not valid"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                    data={
                        "message": "Invalid data"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        order = Orders.objects.create(
            restaurant=restaurant,
            quantity=quantity,
            item=item,
            comments=comments,
        )
        return Response(
            data=OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class OrdersRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET orders/:pk/
    """    
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            order = self.queryset.get(pk=kwargs["pk"])
            return Response(OrderSerializer(order).data)
        except Orders.DoesNotExist:
            return Response(
                data={
                    "message": "Order with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    # TODO: Update and Delete

class OrdersRestaurantListView(generics.ListAPIView):
    """
    GET orders/restaurant/:restaurant
    """
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self): 
        queryset = self.queryset.filter(restaurant=self.kwargs["restaurant"]).order_by("created")
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            Restaurants.objects.get(name=self.kwargs["restaurant"])
        except Restaurants.DoesNotExist:
            return Response(
                data={
                    "message": "Restaurants with name: {} does not exist".format(kwargs["restaurant"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return self.list(request, *args, **kwargs)

class OrdersCustomerListView(generics.ListAPIView):
    """
    GET orders/customer/:customer
    """
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self): 
        queryset = self.queryset.filter(user=self.kwargs["customer"])
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            User.objects.get(pk=self.kwargs["customer"])
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "Customer with id: {} does not exist".format(kwargs["customer"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return self.list(request, *args, **kwargs)

class CostRetrieveView(generics.RetrieveAPIView):
    """
    GET orders/cost/<str:restaurant>
    """    
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            Restaurants.objects.get(name=self.kwargs["restaurant"])
            queryset = self.queryset.filter(restaurant=self.kwargs["restaurant"])
            cost = sum([query.total_price for query in queryset])
            return Response(
                data={
                    "cost": cost
                },
                status=status.HTTP_200_OK
            )
        except Restaurants.DoesNotExist:
            return Response(
                data={
                    "message": "Restaurants with name: {} does not exist".format(kwargs["restaurant"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class AveQuantityRetrieveView(generics.RetrieveAPIView):
    """
    GET orders/stats/average-quantity/<str:restaurant>
    """   
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            Restaurants.objects.get(name=self.kwargs["restaurant"])
            queryset = self.queryset.filter(restaurant=self.kwargs["restaurant"])
            average = sum([query.quantity for query in queryset])/len(queryset)
            return Response(
                data={
                    "average": average
                },
                status=status.HTTP_200_OK
            )
        except Restaurants.DoesNotExist:
            return Response(
                data={
                    "message": "Restaurants with name: {} does not exist".format(kwargs["restaurant"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
