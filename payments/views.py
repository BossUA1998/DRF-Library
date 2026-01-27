from rest_framework import viewsets
from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects

    def get_queryset(self):
        queryset = self.queryset.all()
        if not self.request.user.is_staff:
            return queryset.filter(borrowing__user=self.request.user)
        return queryset
