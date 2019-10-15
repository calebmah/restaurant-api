from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Sum
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrdersRetrieveView(generics.RetrieveAPIView):
    """
    GET orders/:pk/
    """    
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
                    "message": f"Restaurant with name: {kwargs['restaurant']} does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return self.list(request, *args, **kwargs)

class OrdersCustomerListView(generics.ListAPIView):
    """
    GET orders/customer/:customer
    """
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self): 
        queryset = Orders.objects.filter(user=self.kwargs["customer"])
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            User.objects.get(pk=self.kwargs["customer"])
        except User.DoesNotExist:
            return Response(
                data={
                    "message": f"Customer with id: {kwargs['customer']} does not exist"
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
            queryset = self.get_queryset().filter(restaurant=self.kwargs["restaurant"])
            cost = queryset.aggregate(Sum("total_price")).get("total_price__sum")
            return Response(
                data={
                    "cost": cost
                },
                status=status.HTTP_200_OK
            )
        except Restaurants.DoesNotExist:
            return Response(
                data={
                    "message": f"Restaurant with name: {kwargs['restaurant']} does not exist"
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
            queryset = self.get_queryset().filter(restaurant=self.kwargs["restaurant"])
            average = queryset.aggregate(Avg("quantity")).get("quantity__avg")
            return Response(
                data={
                    "average": average
                },
                status=status.HTTP_200_OK
            )
        except Restaurants.DoesNotExist:
            return Response(
                data={
                    "message": f"Restaurant with name: {kwargs['restaurant']} does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
