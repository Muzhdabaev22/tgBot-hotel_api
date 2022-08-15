import requests
import telebot
import json

city = '123'
count_hotels = 0

querystring = {"query": f"{city}", "currency": "USD"}

headers = {
    "X-RapidAPI-Key": "877e7262b9msh80be8ffb3287018p105eacjsnee4a1c0cd717",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

url = requests.get("https://hotels4.p.rapidapi.com/locations/v2/search/", headers=headers, params=querystring)

data = json.loads(url.text)


bot = telebot.TeleBot('5560298708:AAFIb9qv96bGs-j8vAhusqYFP2YYok6PQs4')


@bot.message_handler(commands=['start'])
def start(message):
    """
    Команда для начала работы бота
    """
    bot.send_message(message.from_user.id, 'Привет! Введи команду /help для просмотра списка команд')


@bot.message_handler(commands=['help'])
def help_command(message):
    """
    Команда для вывода всех функций
    """
    bot.send_message(message.from_user.id, 'Список команд: \n'
                                           '● /lowprice — вывод самых дешёвых отелей в городе,\n'
                                           '● /highprice — вывод самых дорогих отелей в городе,\n'
                                           '● /bestdeal — вывод отелей, наиболее подходящих по цене и расположению '
                                           'отцентра,\n '
                                           '● /history — вывод истории поиска отелей.')


@bot.message_handler(commands=['lowprice'])
def lowprice_command(message):
    """
    Команда для начала поиска самых дешёвых отелей
    """
    bot.send_message(message.from_user.id, 'В каком городе будем проводить поиск отелей?')
    bot.register_next_step_handler(message, set_city)


def set_city(message):
    """
      Функция для ввода города, где будет производиться поиск отелей
    """
    global city
    global data

    city = message.text
    if data["moresuggestions"] == 0:  # проверка на наличие предложений
        bot.send_message(message.from_user.id, 'Города с таким названием не существует или в этом городе нет отелей. '
                                               'Повторите попытку')
    else:
        bot.send_message(message.from_user.id, 'Введите количество отелей, которые необходимо вывести в результате')
        bot.register_next_step_handler(message, set_count_hotels)


def set_count_hotels(message):
    """
    Функция для ввода количества отелей, которые в итоге надо будет вывести
    """
    global count_hotels

    while count_hotels == 0:  # проверяем что возраст изменился
        try:
            count_hotels = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

    bot.send_message(message.from_user.id, 'Вывести фотографии или без?(Да/Нет)')
    bot.register_next_step_handler(message, image_function)


def image_function(message):  # в разработке
    """
    Функция для проверки желания пользователя на вывод фотографий к отелю
    """
    if message.text == 'Да':
        bot.send_message(message.from_user.id, 'ещё не готово')
    elif message.text == 'Нет':
        bot.send_message(message.from_user.id, 'выводим..')


bot.polling(none_stop=True)  # python diploma/bot.py
