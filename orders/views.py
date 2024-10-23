from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from lucida.permissions import IsStaff
from .serializers import OrderViewSerializer, OrdersViewSerializer
from orders.models import Order
from users.models import CustomUser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        orders = Order.objects.filter(user=user)

        serializer = OrderViewSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        status = request.data.get("status")
        order = Order.objects.get(id=id)
        order.status = status
        order.save()
        return Response({"msg": "success"})


class AllOrderView(APIView):
    permission_classes = [IsStaff]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrdersViewSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
