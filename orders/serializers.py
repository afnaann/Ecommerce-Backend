from rest_framework import serializers

from users.serializers import UserSerializer
from products.serializers import ProductViewSerializer

from .models import Order, OrderItems


class OrderSerializer(serializers.ModelSerializer):
    product = ProductViewSerializer()

    class Meta:
        model = OrderItems
        fields = ["id", "product", "quantity"]


class OrderViewSerializer(serializers.ModelSerializer):
    order_items = OrderSerializer(many=True, source="orderitems")
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_date",
            "address",
            "total_price",
            "order_items",
            "status",
            "status_display",
        ]

    def get_status_display(self, obj):
        return obj.get_status_display()


class OrdersViewSerializer(serializers.ModelSerializer):
    order_items = OrderSerializer(many=True, source="orderitems")
    user = UserSerializer()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_date",
            "address",
            "total_price",
            "order_items",
            "status",
            "status_display",
        ]

    def get_status_display(self, obj):
        return obj.get_status_display()
