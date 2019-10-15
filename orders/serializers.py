from rest_framework import serializers

from .models import MenuItems, Orders


class OrderSerializer(serializers.ModelSerializer):

    def validate(self, data):
        """
        Check that item is sold by restaurant
        """
        if data['item'].restaurant != data['restaurant']:
            raise serializers.ValidationError(f"{data['restaurant']} does not sell {data['item']}")
        return data

    class Meta:
        model = Orders
        fields = ['id', 'created', 'user', 'restaurant', 'quantity', 'item', 'comments', 'total_price']
