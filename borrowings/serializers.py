from django.db.models import F
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Borrowing.objects.filter(book__inventory__gt=0)
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


class BorrowingDetailSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(read_only=True, slug_field="title")


class EmptySerializer(serializers.Serializer): ...
