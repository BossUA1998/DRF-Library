from datetime import timedelta

from django.utils import timezone
from django_q.tasks import schedule

from payments.models import Payment


def _cancel_payment(payment_session_id):
    try:
        obj = Payment.objects.get(session_id=payment_session_id)
        if obj.status != "PAID":
            obj.status = "CANCELED"
            obj.save()

    except Payment.DoesNotExist:
        print(f"Payment {payment_id} not found")


def schedule_cancel_payment(payment_session_id: int):
    run_time = timezone.now() + timedelta(hours=23)

    schedule(
        func="payments.tasks._cancel_payment",
        payment_session_id=payment_session_id,
        schedule_type="O",
        next_run=run_time,
    )
