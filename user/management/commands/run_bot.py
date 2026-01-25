from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
from django_q.tasks import schedule
from time import sleep
from borrowings.models import Borrowing

bot = TeleBot(settings.TELEGRAM_TOKEN)


def borrowing_notification(chat_id: int, text: str) -> None:
    bot.send_message(chat_id=chat_id, text=text)


def notification_for_telegram_ids():
    borrowings = (
        Borrowing.objects.values("user__telegram_id")
        .filter(user__telegram_id__regex=r"^\d+$")
        .annotate(
            book_list=ArrayAgg("book__title", filter=Q(actual_return_date__isnull=True))
        )
    )
    for borrowing in borrowings:
        borrowing_notification(
            chat_id=borrowing["user__telegram_id"],
            text=f"You have {len(borrowing["book_list"])} books that need to be handed over🥲\n{",".join(borrowing["book_list"])}",
        )
        sleep(0.1)


class Command(BaseCommand):
    help = "Run telegram bot"

    def handle(self, *args, **options):
        @bot.message_handler(commands=["start"])
        def main(message):
            text1 = "Hello, enter the keyword to connect🖐"
            text2 = "To get it, follow the link -> http://localhost:8000/users/telegram/connect/"
            bot.send_message(chat_id=message.chat.id, text=text1)
            bot.send_message(chat_id=message.chat.id, text=text2)

            print(f"COMMAND: /start | send to chat {message.chat.id}")

        @bot.message_handler()
        def connect(message):
            key = message.json["text"]
            user = get_user_model()
            if len(key) == 10 and key.isalpha():
                try:
                    telegram_user = user.objects.get(telegram_id=key)
                    telegram_user.telegram_id = message.from_user.id
                    telegram_user.save()
                except user.DoesNotExist:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text="The key is not yours or it does not exist🥺",
                    )
                except Exception as e:
                    print(type(e), e)
                    bot.send_message(
                        chat_id=message.chat.id,
                        text="Oops, there's an error on our server😞",
                    )
                else:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text="Congratulations, you have been registered🤩",
                    )
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text="This is not a key, must be 10 characters🙄",
                )

        bot.infinity_polling()
