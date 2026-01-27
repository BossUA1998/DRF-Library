import stripe
from django.conf import settings
from django.urls import reverse

from payments.models import Payment

stripe.api_key = settings.STRIPE_PRIVATE_KEY


def create_stripe_session(borrowing: "Borrowing", success_url: str, cancel_url: str):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": borrowing.book.stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url + f"?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=cancel_url + f"?session_id={{CHECKOUT_SESSION_ID}}",
    )

    Payment.objects.create(
        status="PENDING",
        type=session["mode"].upper(),
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=borrowing.book.daily_fee,
    )
