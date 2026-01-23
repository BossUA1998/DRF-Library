from django.db.models import F
from django.db import transaction
from django.utils import timezone

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    EmptySerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            user_id = self.request.query_params.get("user_id")
            is_active = self.request.query_params.get("is_active")

            if user_id:
                queryset = queryset.filter(user_id=user_id)

            if is_active:
                is_active_bool = str(is_active).lower() in ["1", "true"]
                queryset = queryset.filter(actual_return_date__isnull=is_active_bool)
        return queryset

    def get_object(self):
        return self.queryset.get(pk=self.kwargs["pk"], user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
    )
    def borrowing_return(self, request, *args, **kwargs):
        obj = self.get_object()

        with transaction.atomic():
            obj.book.inventory = F("inventory") + 1
            obj.book.save(update_fields=["inventory"])

            obj.actual_return_date = timezone.now().date()
            obj.save(update_fields=["actual_return_date"])

        return Response({"status": "returned"}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingDetailSerializer
        if self.action == "borrowing_return":
            return BorrowingReturnSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
