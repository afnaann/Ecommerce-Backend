from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from lucida.permissions import IsStaff
from .models import CustomUser
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():

            CustomUser.objects.create_user(
                email=serializer.data["email"],
                name=serializer.data["name"],
                password=serializer.data["password"],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginTokenView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class UserView(APIView):
    permission_classes = [IsStaff]
    def get(self, request):
        users = CustomUser.objects.filter(is_staff=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def patch(self, request, id):
        user = get_object_or_404(CustomUser, id=id)

        if not user.is_blocked:
            user.is_blocked = True
            message = 'User has been blocked successfully.'
        else:
            user.is_blocked = False
            message = 'User has been unblocked successfully.'

        user.save()
        return Response({'message': message}, status=status.HTTP_200_OK)