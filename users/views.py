from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'successfully Created'})
        return Response(serializer.errors)
    
    
class LoginTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

