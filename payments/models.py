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

    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    type = models.CharField(max_length=10, choices=TypeChoices.choices)
    borrowing_id = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField(blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
