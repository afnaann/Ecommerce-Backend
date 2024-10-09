from rest_framework import serializers
from .models import CustomUser, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    class Meta:
        model = CustomUser
        fields = ['name','email','password']
    
    def create(self, validated_data):
        name = validated_data.pop('name')
        user = CustomUser.objects.create_user(email=validated_data['email'],password=validated_data['password'])
        try:
            UserProfile.objects.create(user=user,name=name)
        except Exception as e:
            print(e)
            user.delete()
            raise serializers.ValidationError("Error creating user profile.")
        return user
    
  
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        userInfo = UserProfile.objects.get(user=user)
        token['name'] = userInfo.name
        token['email'] = user.email
        token['staff_status'] = user.is_staff
        return token

