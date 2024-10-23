from django.urls import path
from .views import StripeCheckoutView, ProcessOrderView

urlpatterns = [
    path("checkoutsession/", StripeCheckoutView.as_view()),
    path("processorder/", ProcessOrderView.as_view()),
]
