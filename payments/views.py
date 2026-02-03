import stripe

from django.urls import reverse
from django.conf import settings
from django_q.tasks import async_task
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowings.serializers import EmptySerializer
from payments.models import Payment
from payments.serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_PRIVATE_KEY


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects

    def get_queryset(self):
        queryset = self.queryset.select_related("borrowing__book")
        if not self.request.user.is_staff:
            return queryset.filter(borrowing__user=self.request.user)
        return queryset


class PaymentSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if session_id:
            try:
                session = stripe.checkout.Session.retrieve(session_id)
                if (_status := session["payment_status"].upper()) == "PAID":
                    obj = Payment.objects.get(session_id=session_id)
                    if obj.status != "PAID":
                        obj.status = _status
                        obj.save()
                    return Response(
                        data={"success": "Payment made successfully"},
                        status=status.HTTP_200_OK,
                    )
            except stripe.error.InvalidRequestError:
                return Response(
                    data={"success": "Session id failed validation"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        return Response(
            data={"success": "Payment does not exist"}, status=status.HTTP_403_FORBIDDEN
        )


class PaymentCancelView(APIView):
    def get(self, request, *args, **kwargs):
        async_task(
            func="payments.tasks.schedule_cancel_payment",
            payment_session_id=request.GET.get("session_id")
        )
        return Response(data={"canceled": "You will be able to pay for it within 24 hours"}, status=status.HTTP_200_OK)
