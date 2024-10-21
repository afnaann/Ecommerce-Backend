from django.urls import path
from . import views

urlpatterns = [
    path("get/<int:pk>/", views.CartView.as_view()),
    path("post/<int:pk>/", views.CartView.as_view()),
    path("patch/<int:pk>/", views.CartView.as_view()),
]
