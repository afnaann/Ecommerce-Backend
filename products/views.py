from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, ProductViewSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Products, Category
from rest_framework import status

# Create your views here.


class ProductView(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                product = Products.objects.get(id=id)
                serializer = ProductViewSerializer(product)
                return Response(serializer.data)
            except Products.DoesNotExist:
                return Response({"Error": "Product Not Found!"})
        else:
            products = Products.objects.all()
            serializer = ProductViewSerializer(products, many=True)
            return Response(serializer.data)

    # Tried to handle here, but here, the data is being taken from request.data

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Products.objects.get(id=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Products.DoesNotExist:
            return Response(
                {"error": "Product Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, pk):
        try:
            product = Products.objects.get(id=pk)
            serializer = ProductSerializer(
                instance=product, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Products.DoesNotExist:
            return Response(
                {"error": "Product Not Found!"}, status=status.HTTP_404_NOT_FOUND
            )


class CategoryView(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
