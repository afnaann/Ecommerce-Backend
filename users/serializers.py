from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["name"] = user.name
        token["email"] = user.email
        token["staff_status"] = user.is_staff
        token["admin_status"] = user.is_superuser
        token["is_blocked"] = user.is_blocked
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if user.is_blocked:
            raise serializers.ValidationError(
                "Your Account Is Blocked Due To Suspicious Activity."
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "is_blocked"]
