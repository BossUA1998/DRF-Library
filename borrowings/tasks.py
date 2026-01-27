import stripe
from django.conf import settings
from django.urls import reverse

from payments.models import Payment

from decimal import Decimal, ROUND_HALF_UP

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


def create_fine_session(borrowing: "Borrowing", fine_multiplier: int, success_url: str, cancel_url: str):
    missed_days = borrowing.actual_return_date - borrowing.expected_return_date
    print(fine_multiplier, borrowing.book.daily_fee, missed_days.days)
    raw_amount = Decimal(fine_multiplier) * Decimal(borrowing.book.daily_fee) * Decimal(missed_days.days)
    money_to_pay = raw_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"FINE for borrowing book: {borrowing.book.title}",
                },
                "unit_amount": int(money_to_pay * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url + f"?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=cancel_url + f"?session_id={{CHECKOUT_SESSION_ID}}",
    )

    Payment.objects.create(
        status="PENDING",
        type="FINE",
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=money_to_pay,
    )
