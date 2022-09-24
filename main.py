

import telebot
import os
from classes import class_history
from dotenv import load_dotenv
from telebot import types
from utils import locations_v2_search, sorted_lowPrice_list, create_list, get_image, sorted_highPrice_list, \
    search_for_suitablel_bestdeal, get_time

load_dotenv()
TOKEN = os.getenv("TOKEN_BOT")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """
    Команда для начала работы бота
    """
    class_history.setter_for_not_hotels(message.text, get_time())
    bot.send_message(message.from_user.id, 'Привет! Введи команду /help для просмотра списка команд')


@bot.message_handler(commands=['help'])
def help_command(message):
    """
    Команда для вывода всех функций
    """
    class_history.setter_for_not_hotels(message.text, get_time())
    bot.send_message(message.from_user.id, 'Список команд: \n'
                                           '● /lowprice — вывод самых дешёвых отелей в городе,\n'
                                           '● /highprice — вывод самых дорогих отелей в городе,\n'
                                           '● /bestdeal — вывод отелей, наиболее подходящих по цене и расположению '
                                           'от центра,\n '
                                           '● /history — вывод истории поиска отелей.')


@bot.message_handler(commands=['history'])
def history_command(message):
    class_history.setter_for_not_hotels(message.text, get_time())
    history_list = class_history.getter_history()
    try:
        for i_history in range(len(history_list)):
            if len(history_list[i_history]) == 3:
                command, time, hotels = history_list[i_history][0], history_list[i_history][1], history_list[i_history][
                    2]
                bot.send_message(message.from_user.id, f"Команда: {command},\n"
                                                       f"Дата и время: {time}\n"
                                                       f"Выведенные отели: {str(hotels)[1:-1]}")
            else:
                command, time = history_list[i_history][0], history_list[i_history][1]
                bot.send_message(message.from_user.id, f"Команда: {command},\n"
                                                       f"Дата и время: {time}\n")
    except TypeError:
        bot.send_message(message.from_user.id, "Ранее вы ничего не вводили")


@bot.message_handler(commands=['lowprice'])
def lowprice_command(message):
    """
    Команда для начала поиска самых дешёвых отелей
    """
    class_history.setter_command_and_time(message.text, get_time())
    bot.send_message(message.from_user.id, 'Введите город')
    bot.register_next_step_handler(message, low_price_hotels)


@bot.message_handler(commands=['highprice'])
def highprice_command(message):
    """
    Команда для начала поиска самых дорогих отелей
    """
    class_history.setter_command_and_time(message.text, get_time())
    bot.send_message(message.from_user.id, 'Введите город')
    bot.register_next_step_handler(message, high_price_hotels)


@bot.message_handler(commands=['bestdeal'])
def bestdeal_command(message):
    """
    Команда для начала поиска наиболее подходящих по цене и расположению от центра отеля
    """
    class_history.setter_command_and_time(message.text, get_time())
    bot.send_message(message.from_user.id, 'Введите город')
    bot.register_next_step_handler(message, range_price)


def range_price(message):
    """
    Запрос информации о цене
    """
    city = message.text
    bot.send_message(message.from_user.id, 'Введите диапазон цены(В долларах). Пример: 200-300')
    bot.register_next_step_handler(message, range_distance, city)


def range_distance(message, city):
    """
    Запрос информации о диапазоне расстояния от центра
    """
    try:
        price = message.text.split('-')
        bot.send_message(message.from_user.id, 'Введите диапазон расстояния от центра(км). Пример: 2.5-10')
        bot.register_next_step_handler(message, treatment_ranges, city, price)
    except TypeError:
        bot.send_message(message.from_user.id, 'Вы не правильно ввели цену. Пример: 200-300')


def treatment_ranges(message, city, price):  # price в виде списка
    """
    Сортировка списка отелей подходящих по запросам пользователя
    """
    try:
        distance = message.text.split('-')  # дистанция в виде списка
        city_info = locations_v2_search(city)  # получаем информацию об отелях
        list_for_sort = create_list(city_info)  # создал cписок
        sorted_list = search_for_suitablel_bestdeal(list_for_sort, price, distance)  # сортируем список
        bot.send_message(message.from_user.id, f'Сколько вывести отелей? Максимум {len(sorted_list)}')
        bot.register_next_step_handler(message, hotel_max, sorted_list)
    except TypeError:
        bot.send_message(message.from_user.id, 'Вы не правильно ввели диапазон. Пример: 2-5.9')


def high_price_hotels(message):
    """
    Создание и сортировка списка с информацией об дорогих отелях
    """
    data_hotels_in_city = locations_v2_search(message.text)  # получил данные отелей в городе
    list_for_sort = create_list(data_hotels_in_city)  # создал cписок из отелей по id
    sorted_list = sorted_highPrice_list(list_for_sort)  # отсортировал его
    bot.send_message(message.from_user.id, f'Сколько вывести отелей? Максимум {len(sorted_list)}')
    bot.register_next_step_handler(message, hotel_max, sorted_list)


def low_price_hotels(message):
    """
    Создание и сортировка списка с информацией об дешёвых отелях
    """
    data_hotels_in_city = locations_v2_search(message.text)  # получил данные отелей в городе
    list_for_sort = create_list(data_hotels_in_city)  # создал список
    sorted_list = sorted_lowPrice_list(list_for_sort)  # отсортировал его
    bot.send_message(message.from_user.id, f'Сколько вывести отелей? Максимум {len(sorted_list)}')
    bot.register_next_step_handler(message, hotel_max, sorted_list)


def hotel_max(message, sorted_list):
    """
    Вывод названия и цены отеля, запрос о показе фотографий об отеле
    """
    hotel_maximum = message.text
    if hotel_maximum != 0:
        try:
            hotels_list = list()
            for index in range(0, int(hotel_maximum)):
                hotel_name, hotel_price, hotel_id = sorted_list[index][0], sorted_list[index][1], sorted_list[index][2]
                hotels_list.append(hotel_name)
                kb = types.InlineKeyboardMarkup()
                kb.add(types.InlineKeyboardButton('Получить фото', callback_data=f'hotel_{hotel_id}'))
                bot.send_message(message.from_user.id, f'Название: {hotel_name}, \nЦена за ночь: {hotel_price}',
                                 reply_markup=kb)
            class_history.setter_hotels(hotels_list)
            class_history.setter_for_hotels()
        except TypeError:
            bot.send_message(message.from_user.id, 'Похоже вы ввели не число. Пожалуйста, попробуйте снова.')
            class_history.else_setter_for_hotels()
    else:
        class_history.else_setter_for_hotels()
        bot.send_message(message.from_user.id, 'Нет результатов.')


@bot.callback_query_handler(func=lambda call: call.data.startswith('hotel_'))
def image(call):
    """
    Вывод фотографий на экран
    """
    link = get_image(call.data.split('_')[-1])
    bot.send_photo(call.from_user.id, link.format(size='z'))


if __name__ == '__main__':
    bot.polling(none_stop=True)  # python main.py

