import stripe
from django.conf import settings
from library.models import Book


def create_stripe_product(book_id: int):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    book = Book.objects.get(id=book_id)

    product = stripe.Product.create(name=book.title)
    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(book.daily_fee * 100),
        currency="usd",
    )
    book.stripe_product_id = product.id
    book.stripe_price_id = price.id
    book.save()
