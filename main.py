import telebot
import os
from dotenv import load_dotenv
from telebot import types
from utils import locations_v2_search, sorted_lowPrice_list, create_list_lowPrice, get_image


load_dotenv()
TOKEN = os.getenv("TOKEN_BOT")
bot = telebot.TeleBot(TOKEN)


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
    bot.send_message(message.from_user.id, 'Введите город')
    bot.register_next_step_handler(message, low_price_hotels)


def low_price_hotels(message):
    """
    Создание и сортировка списка с информацией об отеле
    """
    data_hotels_in_city = locations_v2_search(message.text)  # получил данные отелей в городе
    dict_for_sort = create_list_lowPrice(data_hotels_in_city)  # создал словарь
    sorted_dict = sorted_lowPrice_list(dict_for_sort)  # отсортировал его
    bot.send_message(message.from_user.id, f'Сколько вывести отелей? Максимум {len(sorted_dict)}')
    bot.register_next_step_handler(message, hotel_max, sorted_dict)


def hotel_max(message, sorted_list):
    """
    Вывод названия и цены отеля, запрос о показе фотографий об отеле
    """
    hotel_maximum = message.text
    try:
        for index in range(0, int(hotel_maximum)):
            hotel_name, hotel_price, hotel_id = sorted_list[index][0], sorted_list[index][1], sorted_list[index][2]
            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton('Получить фото', callback_data=f'hotel_{hotel_id}'))
            bot.send_message(message.from_user.id, f'Название: {hotel_name}, \nЦена за ночь: {hotel_price}', reply_markup=kb)
    except Exception:
        bot.send_message(message.from_user.id, 'Не правильный ввод количества вывода отелей')


@bot.callback_query_handler(func=lambda call: call.data.startswith('hotel_'))
def image(call):
    """
    Вывод фотографий на экран
    """
    link = get_image(call.data.split('_')[-1])
    bot.send_photo(call.from_user.id, link.format(size='z'))


if __name__ == '__main__':
    bot.polling(none_stop=True)  # python main.py
