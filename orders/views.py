from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from lucida.permissions import IsStaff
from .serializers import OrderViewSerializer, OrdersViewSerializer
from orders.models import Order
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:    
            user = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response({'error':'User Does Not Exist'},status=status.HTTP_404_NOT_FOUND)
        
        orders = Order.objects.filter(user=user)
        serializer = OrderViewSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        statuss = request.data.get("status")
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response({'error':'Order Id Does Not Exist'},status=status.HTTP_404_NOT_FOUND)
        order.status = statuss
        order.save()
        return Response({"msg": "success"},status=status.HTTP_201_CREATED)


class AllOrderView(APIView):
    permission_classes = [IsStaff]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrdersViewSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
