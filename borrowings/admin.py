from django.contrib import admin
from django.urls import reverse

from borrowings.models import Borrowing

from django_q.tasks import async_task


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'actual_return_date')

    def save_model(self, request, obj, form, change):
        if not change and not getattr(obj, 'user', None):
            obj.user = request.user

        super().save_model(request, obj, form, change)

        async_task(
            func="borrowings.tasks.create_stripe_session",
            borrowing=Borrowing.objects.get(pk=obj.pk),  # borrowing
            success_url=request.build_absolute_uri(reverse("payments:payment_success")),
            cancel_url=request.build_absolute_uri(reverse("payments:payment_cancel")),
        )
