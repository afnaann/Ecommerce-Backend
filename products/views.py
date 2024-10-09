from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Products
# Create your views here.


class GetProducts(APIView):
    def get(self,request):
        products = Products.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)