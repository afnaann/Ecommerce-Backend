from django.urls import path
from . import views

urlpatterns = [
    path('get/',views.GetProducts.as_view()),

]
