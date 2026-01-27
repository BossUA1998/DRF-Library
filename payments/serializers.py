from rest_framework import serializers

from payments.models import Payment


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "session_url",
            "money_to_pay",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    borrowing = serializers.StringRelatedField(read_only=True)

    class Meta(PaymentDetailSerializer.Meta):
        fields = PaymentDetailSerializer.Meta.fields + ["borrowing", "session_id"]
