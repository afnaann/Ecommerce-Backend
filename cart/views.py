from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Products
from .serializers import CartAddSerializer, CartViewSerializer

from .models import CartItem, Cart
from users.models import CustomUser


class CartView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        try:
            cart = Cart.objects.get(user=user)
            cartItems = CartItem.objects.filter(cart=cart)
            serializer = CartViewSerializer(cartItems, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response(
                {"message": "Cart is empty", "cart": []},
                status=status.HTTP_204_NO_CONTENT,
            )

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        cart, created = Cart.objects.get_or_create(user=user)
        serializer = CartAddSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.data["product"]
            quantity = serializer.data.get("quantity", 1)
            product = get_object_or_404(Products, id=product_id)
            cartItem, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )
            if created:
                cartItem.quantity = quantity
            else:
                if product.stock > cartItem.quantity:
                    cartItem.quantity += quantity
                else:
                    return Response(
                        {"update": "Product Is Out Of Stock!"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            cartItem.save()

            response_serializer = CartViewSerializer(cartItem)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        cart = Cart.objects.get(user=user)
        serializer = CartAddSerializer(data=request.data)
        if serializer.is_valid():

            product_id = serializer.data["product"]
            quantity = serializer.validated_data["quantity"]
            product = get_object_or_404(Products, id=product_id)
            Cart_item = CartItem.objects.get(cart=cart, product=product)

            if quantity == 0:
                Cart_item.delete()
                return Response(serializer.data)
            else:
                if product.stock >= quantity:
                    Cart_item.quantity = quantity
                else:
                    return Response(
                        {"update": "Product Is Out Of Stock!"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            Cart_item.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
