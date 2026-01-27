from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payments.views import PaymentViewSet, PaymentSuccessView, PaymentCancelView

router = DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("cancel/", PaymentCancelView.as_view(), name="payment_cancel"),
    path("", include(router.urls)),
]

app_name = "payments"
