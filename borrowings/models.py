from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from library.models import Book
from django.conf import settings


def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError("The date must not be in the past")


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(validators=[validate_date])
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.expected_return_date is None:
            self.full_clean()
        return super().save(*args, **kwargs)
