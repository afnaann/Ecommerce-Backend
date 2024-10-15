from django.urls import path
from . import views

urlpatterns = [
    path('get/',views.ProductView.as_view()),
    path('get/<int:id>/',views.ProductView.as_view()),
    path('post/',views.ProductView.as_view()),
    path('delete/<int:pk>/',views.ProductView.as_view()),
    path('update/<int:pk>/',views.ProductView.as_view()),
    
    path('category/get/',views.CategoryView.as_view()),
]
