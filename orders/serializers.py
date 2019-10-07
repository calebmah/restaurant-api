from rest_framework import serializers

from .models import Orders


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'created', 'user', 'restaurant', 'quantity','item','comments','total_price']
