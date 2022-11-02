from telebot import types
from database.classes import class_history
from utils_directory.utils import locations_v2_search, create_list_without_CITYGROUP, sorted_lowPrice_list, \
    sorted_highPrice_list, create_list_with_CITYGROUP_low, create_list_with_CITYGROUP_high, get_image_photo
from database.setting import bot


def low_price_hotel(message, locale):
    """
    Информация о заезде и выезде в отель
    """
    bot.send_message(message.from_user.id, text="Обрабатываем запрос...")
    try:
        data_hotels_in_city = locations_v2_search(message.text, locale)  # получил данные отелей в городе

        if len(data_hotels_in_city["suggestions"][0]["entities"]) != 0:  # проверка на наличие "city_group" в api
            kb = types.InlineKeyboardMarkup(row_width=1)
            for i_kb in range(len(data_hotels_in_city["suggestions"][0]["entities"])):  # создал кнопки с местами
                kb.add(types.InlineKeyboardButton(data_hotels_in_city["suggestions"][0]["entities"][i_kb]["name"],
                                                  callback_data=
                                                  f"citygroupLOW_{data_hotels_in_city['suggestions'][0]['entities'][i_kb]['destinationId']}_{locale}"))
            bot.send_message(message.from_user.id, "Уточните место:", reply_markup=kb)

        else:
            if len(data_hotels_in_city["suggestions"][1]["entities"]) != 0:
                for_continue_without_CITYGROUP(message, data_hotels_in_city)
            else:
                class_history.else_setter_for_hotels()
                bot.send_message(message.from_user.id, "Результатов не найдено")

    except TypeError:
        bot.send_message(message.from_user.id, "Результатов не найдено")


def high_price_hotels(message, locate):
    """
    Информация о заезде и выезде в отель
    """
    bot.send_message(message.from_user.id, text="Обрабатываем запрос...")
    try:
        data_hotels_in_city = locations_v2_search(message.text, locate)  # получил данные отелей в городе

        if len(data_hotels_in_city["suggestions"][0]["entities"]) != 0:  # проверка на наличие "city_group" в api
            kb = types.InlineKeyboardMarkup(row_width=1)
            for i_kb in range(len(data_hotels_in_city["suggestions"][0]["entities"])):  # создал кнопки с местами
                kb.add(types.InlineKeyboardButton(data_hotels_in_city["suggestions"][0]["entities"][i_kb]["name"],
                                                  callback_data=
                                                  f"citygroupHIGH_{data_hotels_in_city['suggestions'][0]['entities'][i_kb]['destinationId']}_{locate}"))
            bot.send_message(message.from_user.id, "Уточните место:", reply_markup=kb)

        else:
            if len(data_hotels_in_city["suggestions"][1]["entities"]) != 0:
                for_continue_without_CITYGROUP(message, data_hotels_in_city)
            else:
                class_history.else_setter_for_hotels()
                bot.send_message(message.from_user.id, "Результатов не найдено")

    except Exception:
        bot.send_message(message.from_user.id, "Результатов не найдено")


def best_deal_hotel(message, locate):
    """
    Информация о заезде и выезде в отель
    """
    bot.send_message(message.from_user.id, text="Обрабатываем запрос...")
    try:
        data_hotels_in_city = locations_v2_search(message.text, locate)  # получил данные отелей в городе

        if len(data_hotels_in_city["suggestions"][0]["entities"]) != 0:  # проверка на наличие "city_group" в api
            kb = types.InlineKeyboardMarkup(row_width=1)
            for i_kb in range(len(data_hotels_in_city["suggestions"][0]["entities"])):  # создал кнопки с местами
                kb.add(types.InlineKeyboardButton(data_hotels_in_city["suggestions"][0]["entities"][i_kb]["name"],
                                                  callback_data=
                                                  f"citygroupBEST_{data_hotels_in_city['suggestions'][0]['entities'][i_kb]['destinationId']}_{locate}"))
            bot.send_message(message.from_user.id, "Уточните место:", reply_markup=kb)

        else:
            if len(data_hotels_in_city["suggestions"][1]["entities"]) != 0:
                for_continue_without_CITYGROUP(message, data_hotels_in_city)
            else:
                class_history.else_setter_for_hotels()
                bot.send_message(message.from_user.id, "Результатов не найдено")

    except Exception:
        bot.send_message(message.from_user.id, "Результатов не найдено")


def with_photo_questionLOW(call, place, locale):
    if call.text.lower() == "да" or call.text.lower() == "yes":
        for_continue_lowprice_with_CITYGROUP(call, place, locale, "yes")
    elif call.text.lower() == "нет" or call.text.lower() == "no":
        for_continue_lowprice_with_CITYGROUP(call, place, locale, "no")
    else:
        bot.send_message(call.message.from_user.id, "Я вас не понимаю. Введите 'Да' или 'Нет'.")
        bot.register_callback_query_handler(call.chat, with_photo_questionLOW, place, locale)


def with_photo_questionHIGH(call, place, locale):
    if call.text.lower() == "да" or call.text.lower() == "yes":
        for_continue_highprice_with_CITYGROUP(call, place, locale, "yes")
    elif call.text.lower() == "нет" or call.text.lower() == "no":
        for_continue_highprice_with_CITYGROUP(call, place, locale, "no")
    else:
        bot.send_message(call.message.from_user.id, "Я вас не понимаю. Введите 'Да' или 'Нет'.")
        bot.register_callback_query_handler(call.chat, with_photo_questionHIGH, place, locale)


def with_photo_questionBEST(call, place, locale):
    if call.text.lower() == "да" or call.text.lower() == "yes":
        bot.send_message(call.from_user.id, "Введите диапазон цен (в долларах). Пример: 200-300")
        bot.register_next_step_handler(call, for_continue_bestdeal_PRICE, place, locale, "yes")
    elif call.text.lower() == "нет" or call.text.lower() == "no":
        bot.send_message(call.from_user.id, "Введите диапазон цен (в долларах). Пример: 200-300")
        bot.register_next_step_handler(call, for_continue_bestdeal_PRICE, place, locale, "no")
    else:
        bot.send_message(call.from_user.id, "Я вас не понимаю. Введите 'Да' или 'Нет'.")
        bot.register_callback_query_handler(call.chat, with_photo_questionHIGH, place, locale)


def for_continue_highprice_with_CITYGROUP(call, place, locale, answer_photo):
    """
    Продолжение функции highprice: создания и сортировки списка отелей
    c city_group
    """
    bot.send_message(call.from_user.id, "Обрабатываем запрос...")
    list_for_sort = create_list_with_CITYGROUP_high(place, locale)  # создал список
    try:
        sorted_list = sorted_highPrice_list(list_for_sort)  # отсортировал его
        bot.send_message(call.from_user.id, f'Сколько вывести отелей? Максимум {len(sorted_list)}')
        bot.register_next_step_handler(call, hotel_max_with_CITYGROUP, sorted_list, answer_photo)
    except TypeError:
        bot.send_message(call.from_user.id, f'Сколько вывести отелей? Максимум {len(list_for_sort)}')
        bot.register_next_step_handler(call, hotel_max_with_CITYGROUP, list_for_sort, answer_photo)


def for_continue_lowprice_with_CITYGROUP(call, place, locale, answer_photo):
    """
    Продолжение функции lowprice: создания и сортировки списка отелей
    c city_group
    """
    bot.send_message(call.from_user.id, "Обрабатываем запрос...")
    list_for_sort = create_list_with_CITYGROUP_low(place, locale)  # создал список
    try:
        sorted_list = sorted_lowPrice_list(list_for_sort)  # отсортировал его
        bot.send_message(call.from_user.id, f'Сколько вывести отелей? Максимум {len(sorted_list)}')
        bot.register_next_step_handler(call, hotel_max_with_CITYGROUP, sorted_list, answer_photo)
    except TypeError:
        bot.send_message(call.from_user.id, f'Сколько вывести отелей? Максимум {len(list_for_sort)}')
        bot.register_next_step_handler(call, hotel_max_with_CITYGROUP, list_for_sort, answer_photo)


def for_continue_bestdeal_PRICE(message, place, locale, answer_photo):
    try:
        price = message.text.split("-")
        bot.send_message(message.from_user.id, "Введите диапазон расстояния до центра(в км). Пример: 2-30")
        bot.register_next_step_handler(message, for_continue_bestdeal_DISTANCE, place, locale, answer_photo, price)
    except TypeError:
        bot.send_message("Вы ввели не правильно диапазон цен. Введите диапазон ещё раз. Пример: 200-300")
        bot.register_next_step_handler(message, for_continue_bestdeal_PRICE, place, locale, answer_photo)


def for_continue_without_CITYGROUP(message, data):
    """
    Продолжение функции lowprice: создания и сортировки списка отелей
    без city_group
    """
    list_hotels = create_list_without_CITYGROUP(data)  # создал список
    bot.send_message(message.from_user.id, f'Сколько вывести отелей? Максимум {len(list_hotels)}')
    bot.register_next_step_handler(message, hotel_max_without_CITYGROUP, list_hotels)


def for_continue_bestdeal_DISTANCE(message, place, locale, answer_photo, price):
    try:
        distance = message.text.split("-")
        bot.send_message(message.from_user.id, "Обрабатываем запрос...")
        # requirements_processing(message, place, locale, answer_photo, price, distance)
    except TypeError:
        bot.send_message("Вы ввели не правильно диапазон расстояния до центра. Введите диапазон ещё раз. Пример: "
                         "2-10")
        bot.register_next_step_handler(message, for_continue_bestdeal_DISTANCE, place, locale, answer_photo, price)


def requirements_processing(message, place, locale, answer_photo, price, distance):
    pass


def hotel_max_with_CITYGROUP(message, sorted_list, answer_hotel):
    """
    Вывод названия и цены отеля, запрос о показе фотографий об отеле
    """
    hotel_maximum = message.text
    try:
        hotels_list = list()
        if answer_hotel == "no":
            for index in range(0, int(hotel_maximum)):
                hotel_name, hotel_price, hotel_id, address = sorted_list[index][0], sorted_list[index][1], \
                                                             sorted_list[index][2], sorted_list[index][3]
                hotels_list.append(hotel_name)
                bot.send_message(message.from_user.id, f'Название: {hotel_name}, '
                                                       f'\nЦена за ночь: {hotel_price}, '
                                                       f'\nАдрес: {address}, '
                                                       f'\nБольше информации на сайте: '
                                                       f'https://www.hotels.com/ho{hotel_id}')
        else:
            for index in range(0, int(hotel_maximum)):
                hotel_name, hotel_price, hotel_id, address = sorted_list[index][0], sorted_list[index][1], \
                                                             sorted_list[index][2], sorted_list[index][3]
                bot.send_media_group(message.chat.id, get_image_photo(hotel_id))
                hotels_list.append(hotel_name)
                bot.send_message(message.from_user.id, f'Название: {hotel_name}, '
                                                       f'\nЦена за ночь: {hotel_price}, '
                                                       f'\nАдрес: {address}, '
                                                       f'\nБольше информации на сайте: '
                                                       f'https://www.hotels.com/ho{hotel_id}')

        class_history.setter_hotels(hotels_list)
        class_history.setter_for_hotels()
    except TypeError:
        bot.send_message(message.from_user.id, 'Похоже вы ввели не число. Пожалуйста, попробуйте снова.')
        class_history.else_setter_for_hotels()


def hotel_max_without_CITYGROUP(message, list_hotels):
    hotel_maximum = message.text
    try:
        hotels_list = list()
        bot.send_message(message.from_user.id, "В связи с санкциями в нашей базе данных есть только названия "
                                               "отелей России. Просим отнестись с пониманием")
        for index in range(0, int(hotel_maximum)):
            hotel_name = list_hotels[index]
            bot.send_message(message.from_user.id, hotel_name)
            hotels_list.append(hotel_name)

        class_history.setter_hotels(hotels_list)
        class_history.setter_for_hotels()
    except TypeError:
        bot.send_message(message.from_user.id, 'Похоже вы ввели не число. Пожалуйста, попробуйте снова.')
        class_history.else_setter_for_hotels()
