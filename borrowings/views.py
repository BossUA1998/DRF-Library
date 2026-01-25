from datetime import datetime

from django_q.tasks import async_task

from django.db.models import F
from django.db import transaction
from django.utils import timezone
from django.utils.dateformat import format as django_format

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    EmptySerializer,
)

from library.models import Book

FUNC_LOCATION = "user.management.commands.run_bot.borrowing_notification"


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            user_id = self.request.query_params.get("user_id")
            is_active = self.request.query_params.get("is_active")

            if user_id and self.request.user.is_staff:
                queryset = queryset.filter(user_id=user_id)

            if is_active:
                is_active_bool = str(is_active).lower() in ["1", "true"]
                queryset = queryset.filter(actual_return_date__isnull=is_active_bool)
        return (
            queryset
            if self.request.user.is_staff
            else queryset.filter(user=self.request.user)
        )

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

        response = Response({"status": "returned"}, status=status.HTTP_200_OK)
        if (chat_id := request.user.telegram_id).isdigit():
            async_task(
                func=FUNC_LOCATION,
                chat_id=chat_id,
                text=f"The return of the book {self.get_object().book.__str__()} was recorded🤗",
            )

        return response

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingDetailSerializer
        if self.action == "borrowing_return":
            return EmptySerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            if (chat_id := request.user.telegram_id).isdigit():
                async_task(
                    func=FUNC_LOCATION,
                    chat_id=chat_id,
                    text=f"Your book {self.get_object().book.__str__()} has been reserved☺️\n"
                    f"You must return it on "
                    f"{django_format(datetime.strptime("01.12.25", "%d.%m.%y"), 'j E Y')}",
                )
        return response
