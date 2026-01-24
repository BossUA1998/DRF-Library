from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot

# from django_q.tasks import async_task

bot = TeleBot(settings.TELEGRAM_TOKEN)


class Command(BaseCommand):
    help = "Run telegram bot"

    def handle(self, *args, **options):
        @bot.message_handler(commands=["start"])
        def main(message):
            text1 = "Hello, enter the keyword to connect🖐"
            text2 = "To get it, follow the link -> http://127.0.0.1:8000/users/telegram/connect/"
            bot.send_message(message.chat.id, text1)
            bot.send_message(message.chat.id, text2)

            print(f"COMMAND: /start | send to chat {message.chat.id}")

        @bot.message_handler()
        def connect(message):
            key = message.json["text"]
            user = get_user_model()
            if len(key) == 10:
                try:
                    telegram_user = user.objects.get(telegram_id=key)
                    telegram_user.telegram_id = message.from_user.id
                    telegram_user.save()
                except user.DoesNotExist:
                    bot.send_message(
                        message.chat.id, "The key is not yours or it does not exist🥺"
                    )
                except Exception as e:
                    print(type(e), e)
                    bot.send_message(
                        message.chat.id, "Oops, there's an error on our server😞"
                    )
                else:
                    bot.send_message(
                        message.chat.id, "Congratulations, you have been registered🤩"
                    )
            else:
                bot.send_message(
                    message.chat.id, "This is not a key, must be 10 characters🙄"
                )

        bot.infinity_polling()
