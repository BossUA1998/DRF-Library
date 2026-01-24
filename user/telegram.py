import telebot
import os

from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))


@bot.message_handler(commands=["start"])
def main(message):
    text1 = "Привіт, введи ключове слово для з'єднання"
    text2 = "Щоб отримати перейди за посиланням http://127.0.0.1:8000/users/telegram/connect/"
    bot.send_message(message.chat.id, text1)
    bot.send_message(message.chat.id, text2)

    print(f'COMMAND: /start | send to {message.chat.id}')


@bot.message_handler()
def connect(message):
    key = message.json["text"]
    try:
        get_user_model().objects.get(telegram_id=key)
    except Exception as e:
        print(type(e).__name__, e)

bot.infinity_polling()
