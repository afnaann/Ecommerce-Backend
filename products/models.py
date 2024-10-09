from django.db import models

# Create your models here.
    
class Category(models.Model):
    type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.type
    

class Products(models.Model):
    name = models.CharField(max_length=100)
    ImageLink = models.URLField(max_length=500)
    ImageAlt = models.CharField(max_length=50)
    price = models.IntegerField()
    color = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    