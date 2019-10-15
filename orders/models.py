from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Restaurants(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class MenuItems(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255, null=False, unique=True)
    price = models.DecimalField(max_digits=32, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return f"{self.restaurant}: {self.name} - {self.price}"

class Orders(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, to_field="name")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    item = models.ForeignKey(MenuItems, on_delete=models.CASCADE, to_field="name")
    comments = models.CharField(max_length=255, blank=True)
    total_price = models.DecimalField(max_digits=32, decimal_places=2, editable = False, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return f"{self.restaurant} Orders: {self.quantity} x {self.item} at {self.created}"

    def save(self, *args, **kwargs):
        item = MenuItems.objects.get(pk=self.item.id)
        self.total_price = self.quantity * item.price
        super().save(*args, **kwargs) 

    def clean(self):
        """
        Check that item is sold by restaurant (for admin)
        """  
        if self.item.restaurant != self.restaurant:
            raise ValidationError(f"{self.restaurant} does not sell {self.item}")
