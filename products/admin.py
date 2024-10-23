from django.contrib import admin
from .models import Products, Category

# Register your models here.

admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock")


admin.site.register(Products, ProductAdmin)
