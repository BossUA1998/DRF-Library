from django.db import models
from borrowings.models import Borrowing
from django.utils.text import gettext_lazy as _


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")

    class TypeChoices(models.TextChoices):
        PAYMENT = "PAYMENT", _("Payment")
        FINE = "FINE", _("Fine")

    status = models.CharField(choices=StatusChoices.choices)
    type = models.CharField(choices=TypeChoices.choices)
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.CharField(max_length=1024, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
