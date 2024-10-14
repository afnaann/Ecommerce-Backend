import base64
from rest_framework import serializers

from .models import Products,Category


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True,required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Products
        fields = ['name','image','Image_base64','stock','price','category']
        extra_kwargs = {
            'Image_base64':{'read_only':True}
        }
    
    def create(self, validated_data):
        image = validated_data.pop('image',None)
        if image:
            Image_base64 = base64.b64encode(image.read()).decode('utf-8')
            validated_data['Image_base64'] = Image_base64
        
        return Products.objects.create(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class ProductViewSerializer(serializers.ModelSerializer):    
    category = CategorySerializer()
    class Meta:
        model = Products
        fields = ['name','Image_base64','stock','price','category','id']

