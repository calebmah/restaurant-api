from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import (AveQuantityRetrieveView, CostRetrieveView,
                    OrdersCustomerListView, OrdersListCreateView,
                    OrdersRestaurantListView, OrdersRetrieveView)

urlpatterns = [
    path('orders/', OrdersListCreateView.as_view(), name="orders-all"),
    path('orders/<int:pk>/', OrdersRetrieveView.as_view(), name="orders-single"),
    path('orders/restaurant/<str:restaurant>/', OrdersRestaurantListView.as_view(), name="orders-restaurant"),
    path('orders/customer/<int:customer>/', OrdersCustomerListView.as_view(), name="orders-customer"),
    path('orders/cost/<str:restaurant>', CostRetrieveView.as_view(), name="cost-single"),
    path('orders/stats/average-quantity/<str:restaurant>', AveQuantityRetrieveView.as_view(), name="average-quantity"),
    path('auth/token/', obtain_jwt_token, name="generate-token"),
]
