from django.db.models import F
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing, Book
from payments.models import Payment
from payments.serializers import PaymentDetailSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.filter(inventory__gt=0)
    )

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
        ]

    def validate_book(self, book):
        if book.inventory <= 0:
            raise ValidationError("The book inventory must be greater than 0")
        return book

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory = F("inventory") - 1
        book.save()

        book.refresh_from_db()
        return super().create(validated_data)


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(read_only=True, slug_field="title")
    payments_status = serializers.SlugRelatedField(
        read_only=True, slug_field="status", source="payments", many=True
    )

    class Meta(BorrowingSerializer.Meta):
        fields = BorrowingSerializer.Meta.fields + [
            "actual_return_date",
            "payments_status",
        ]


class BorrowingDetailSerializer(BorrowingListSerializer):
    payments_status = None
    payments = PaymentDetailSerializer(many=True, read_only=True)

    class Meta(BorrowingListSerializer.Meta):
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
            "actual_return_date",
            "payments",
        )


class EmptySerializer(serializers.Serializer): ...
