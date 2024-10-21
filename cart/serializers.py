from rest_framework import serializers

from products.models import Products
from products.serializers import ProductViewSerializer

from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["user"]


class CartViewSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    product = ProductViewSerializer()

    class Meta:
        model = CartItem
        fields = ["cart", "product", "quantity"]


class CartAddSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all())

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]
