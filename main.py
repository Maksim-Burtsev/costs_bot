from datetime import date

import telebot
from telebot import types

from services_class import Service


service = Service()

TOKEN = '5344421271:AAHNQluMJLVp4t7TNzQ3uVrBtmVJQPIonIQ'
MY_ID = 458294985
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


@bot.message_handler(commands=['refresh'])
def refresh(message):
    if message.chat.id == MY_ID:
        file = open('costs.csv')
        bot.send_document(message.chat.id, file)
        service.refresh_csv_file()
        bot.send_message(message.chat.id, 'Refreshed')


@bot.message_handler(commands=['get_file'])
def get_file(message):
    if message.chat.id == MY_ID:
        file = open('costs.csv')
        bot.send_document(message.chat.id, file)


@bot.message_handler(commands=['get_log'])
def get_log(message):
    if message.chat.id == MY_ID:
        file = open('logs/degug.log')
        bot.send_document(message.chat.id, file)


@bot.message_handler(content_types='text')
def main(message):
    if message.chat.id == MY_ID:
        if message.text == 'Статистика за неделю':
            week_num = date.today().isocalendar().week
            response_text = service.get_week_statics(week_num)
            bot.send_message(message.chat.id, response_text)

        elif message.text == "Отчёт за всё время":
            response_text = service.get_all_statics()
            bot.send_message(message.chat.id, response_text)
        else:
            text = message.text
            text = text.split()
            if len(text) == 2 and text[0].isalpha() and text[1].isdigit():
                name = text[0]
                price = int(text[1])
                service.add_buy(name, price)
                bot.send_message(message.chat.id, 'Accepted')
            elif len(text) == 2 and text[1].isalpha() and text[0].isdigit():
                name = text[1]
                price = int(text[0])
                service.add_buy(name, price)
                bot.send_message(message.chat.id, 'Accepted')
            else:
                bot.send_message(message.chat.id, 'Dismissed')


bot.infinity_polling()
