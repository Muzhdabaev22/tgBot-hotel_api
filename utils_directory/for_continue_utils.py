from telebot import types
from database.classes import class_history
from utils_directory.utils import locations_v2_search, create_list, sorted_lowPrice_list, sorted_highPrice_list, \
    search_for_suitablel_bestdeal
from database.setting import bot


def low_price_hotels(message):
    """
    Создание и сортировка списка с информацией об дешёвых отелях
    """
    data_hotels_in_city = locations_v2_search(message.text)  # получил данные отелей в городе
    list_for_sort = create_list(data_hotels_in_city)  # создал список
    sorted_list = sorted_lowPrice_list(list_for_sort)  # отсортировал его
    bot.send_message(message.from_user.id, f'Сколько вывести отелей? Максимум {len(sorted_list)}')
    bot.register_next_step_handler(message, hotel_max, sorted_list)


def high_price_hotels(message):
    """
    Создание и сортировка списка с информацией об дорогих отелях
    """
    data_hotels_in_city = locations_v2_search(message.text)  # получил данные отелей в городе
    list_for_sort = create_list(data_hotels_in_city)  # создал cписок из отелей по id
    sorted_list = sorted_highPrice_list(list_for_sort)  # отсортировал его
    bot.send_message(message.from_user.id, f'Сколько вывести отелей? Максимум {len(sorted_list)}')
    bot.register_next_step_handler(message, hotel_max, sorted_list)


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
