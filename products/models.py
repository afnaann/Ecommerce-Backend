from django.db import models
import base64
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100)
    Image_base64 = models.TextField(max_length=500, null=True)
    stock = models.PositiveSmallIntegerField(null=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def set_image(self, image):
        with open(image, "rb") as image_file:
            self.Image_base64 = base64.b64encode(image_file.read().decode("utf-8"))

    def get_image(self):
        return base64.b64decode(self.Image_base64)

    def __str__(self):
        return self.name
