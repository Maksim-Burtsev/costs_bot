import os
from datetime import date

import telebot
from telebot import types
from dotenv import load_dotenv

from services import get_static, add_buy


load_dotenv()
TOKEN = os.getenv('TOKEN')
MY_ID = int(os.getenv('MY_ID'))

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == MY_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Статистика за неделю')
        item2 = types.KeyboardButton("Отчёт за всё время")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, 'Поехали!', reply_markup=markup)


@bot.message_handler(content_types='text')
def main(message):
    if message.chat.id == MY_ID:
        if message.text == 'Статистика за неделю':
            week_number = date.today().isocalendar().week
            message_text = get_static(week_number=week_number)
            bot.send_message(message.chat.id, message_text)

        elif message.text == "Отчёт за всё время":
            message_text = get_static()
            bot.send_message(message.chat.id, message_text)
        else:
            text = message.text
            text = text.split()
            if len(text) == 2 and text[0].isalpha() and text[1].isdigit():
                name = text[0]
                price = int(text[1])
                add_buy(name, price)
                bot.send_message(message.chat.id, 'Accepted')
            elif len(text) == 2 and text[1].isalpha() and text[0].isdigit():
                name = text[1]
                price = int(text[0])
                add_buy(name, price)
                bot.send_message(message.chat.id, 'Accepted')
            else:
                bot.send_message(message.chat.id, 'Dismissed')


bot.infinity_polling()
