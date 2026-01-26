from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import async_task
from library.models import Book


@receiver(post_save, sender=Book)
def create_stripe_product(instance, created, **kwargs):
    if created:
        async_task(
            func="library.tasks.create_stripe_product",
            book_id=instance.id,
        )
