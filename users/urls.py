from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',views.RegisterView.as_view()),
    path('login/',views.LoginTokenView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
