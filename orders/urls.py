from django.urls import path
from . import views

urlpatterns = [
    path("get/<int:pk>/", views.OrderView.as_view()),
    path("get/", views.AllOrderView.as_view()),
    path("update/<int:id>/", views.OrderView.as_view()),
]
