from config2 import token
import telebot
from telebot.types import Message
import requests
import os, sys
from requests.exceptions import ConnectionError, ReadTimeout
import logging

logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s', filemode="w", encoding='utf-8')

bot = telebot.TeleBot(token)
cash = 0
url = 'https://v6.exchangerate-api.com/v6/eec7b5c7194912fb64ea5c6b/latest/USD'
try:
    response = requests.get(url)
    data = response.json()
    logging.info('Успешный запрос к сайту.')
except Exception as e:
    print(f"Произошла ошибка: {e}")
    logging.error(f"Произошла ошибка: {e}")


@bot.message_handler(['start'])
def start(msg: Message):
    bot.send_message(msg.chat.id,
                     "Приветствую! Я бот который конвертирует валюту.\nНажми на /help чтобы узнать о функционале.")
    logging.info(f"Пользователь {msg.from_user.username} запустил бота.")


@bot.message_handler(['help'])
def help(msg: Message):
    bot.send_message(msg.chat.id, "С помощью команды /convert конвертировать заданную сумму из одной валюты в другую\n"
                                  "Пример использования - /convert 100 USD to EUR")


@bot.message_handler(content_types=['text'])
def func(message):
    global cash
    # условие заказчика, чтобы запрос на конвертацию начинался с /convert
    if message.text[:8] == '/convert':
        mess = message.text[9::].split()
        if mess:
            try:
                cash = float(mess[0])
                if cash > 0:
                    if mess[1] in data['conversion_rates'] and mess[3] in data['conversion_rates']:
                        if mess[1] == 'USD':
                            bot.send_message(message.chat.id, round(cash * data["conversion_rates"][mess[3]], 2))
                        else:
                            cash = cash / data["conversion_rates"][mess[1]]
                            bot.send_message(message.chat.id, round(cash * data["conversion_rates"][mess[3]], 2))
                        logging.info(f'Пользователь {message.from_user.username} получил результат.')



                    else:
                        bot.send_message(message.chat.id, f'Вы ввели неверное название валюты')
                else:
                    bot.send_message(message.chat.id, 'Введите число больше нуля')
            except ValueError:
                bot.send_message(message.chat.id, 'Неверный формат, сумму для конвертации вводите числами!')
        else:
            bot.send_message(message.chat.id, "Пример использования - /convert 100 USD to EUR")






    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'привет')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'пока')
    else:
        bot.send_message(message.chat.id, 'я бот для конвертации, не жди от меня многого)')


try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
