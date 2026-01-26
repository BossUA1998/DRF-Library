import stripe
from django.conf import settings
from payments.models import Payment

stripe.api_key = settings.STRIPE_PRIVATE_KEY

def create_stripe_session(borrowing: "Borrowing"):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": borrowing.book.stripe_price_id,
            "quantity": 1,
        }],
        mode='subscription',

        success_url=f"{settings.DOMAIN_NAME}/payment/success",
        cancel_url=f"{settings.DOMAIN_NAME}/payment/cancel",

        # metadata={}
    )

    Payment.objects.create(
        status="PENDING",
        type="PAYMENT",
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=borrowing.book.daily_fee,
    )