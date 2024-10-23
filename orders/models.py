from django.db import models

from products.models import Products
from users.models import CustomUser

# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [
        ("SH", "Shipping"),
        ("OR", "Order Received"),
        ("CA", "Cancelled"),
        ("RT", "Returned"),
        ("RF", "Refunded"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="SH")

    def __str__(self):
        return f"{self.user.name}'s Orders"


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order, related_name="orderitems", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (
            f'{self.order.user.name}"s order of {self.product.name} of {self.quantity}'
        )
