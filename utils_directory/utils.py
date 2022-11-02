import datetime
import json
import requests
from telebot import types

from database.setting import headers
from bs4 import BeautifulSoup


def locations_v2_search(city, locale):
    """
    Получаем информацию о отелях в городе
    """
    querystring = {"query": city, "locale": locale}
    url = requests.get("https://hotels4.p.rapidapi.com/locations/v2/search/", headers=headers, params=querystring)
    data = json.loads(url.text)

    return data


def properties_listLOW(place, locale):
    querystring = {"destinationId": place, "pageNumber": "1", "pageSize": "25", "checkIn": "2023-11-19",
                   "checkOut": "2023-11-22", "adults1": "1", "sortOrder": "PRICE", "locale": locale}

    url = requests.get("https://hotels4.p.rapidapi.com/properties/list", headers=headers, params=querystring)
    data_list = json.loads(url.text)
    return data_list


def properties_listHIGH(place, locale):
    querystring = {"destinationId": place, "pageNumber": "1", "pageSize": "25", "checkIn": "2023-11-19",
                   "checkOut": "2023-11-22", "adults1": "1", "sortOrder": "PRICE_HIGHEST_FIRST", "locale": locale}

    url = requests.get("https://hotels4.p.rapidapi.com/properties/list", headers=headers, params=querystring)
    data_list = json.loads(url.text)
    return data_list


def get_details_about_hotels_with_CITYGROUP(data_hotels, level):
    try:
        name = data_hotels["data"]["body"]["searchResults"]["results"][level]["name"]
        price = data_hotels["data"]["body"]["searchResults"]["results"][level]["ratePlan"]["price"]["current"]
        id_hotel = data_hotels["data"]["body"]["searchResults"]["results"][level]["id"]
        address = data_hotels["data"]["body"]["searchResults"]["results"][level]["address"]["streetAddress"]
        result = [name, price, id_hotel, address]
        return result
    except Exception:
        return None


def create_list_without_CITYGROUP(hotels_data_id):
    """
    Делает список из списков с отелями
    """
    list_info_about_hotel = list()
    for i in range(0, len(hotels_data_id["suggestions"][1]["entities"])):
        name = hotels_data_id["suggestions"][1]["entities"][i]["name"]
        list_info_about_hotel.append(name)
    return list_info_about_hotel


def create_list_with_CITYGROUP_low(place, locale):
    hotels_data = properties_listLOW(place, locale)
    list_info_about_hotel = list()
    for i in range(0, len(hotels_data["data"]["body"]["searchResults"]["results"])):
        list_info_about_hotel.append(get_details_about_hotels_with_CITYGROUP(hotels_data, i))
    return list_info_about_hotel


def create_list_with_CITYGROUP_high(place, locale):
    hotels_data = properties_listHIGH(place, locale)
    list_info_about_hotel = list()
    for i in range(0, len(hotels_data["data"]["body"]["searchResults"]["results"])):
        list_info_about_hotel.append(get_details_about_hotels_with_CITYGROUP(hotels_data, i))
    return list_info_about_hotel


def sorted_lowPrice_list(list_info):
    """
    Сортирует получаемый список по возрастанию цены отеля.
    """
    sorted_list = sorted(list_info, key=lambda x: x[1])
    return sorted_list


def sorted_highPrice_list(list_info):
    """
    Сортирует получаемый список по убыванию цены отеля.
    """
    sorted_list = sorted(list_info, key=lambda x: x[1], reverse=True)
    return sorted_list


def get_image_photo(id_hotel):
    """
    Функция для получения фотографии
    """
    querystring = {"id": id_hotel}

    url = requests.get("https://hotels4.p.rapidapi.com/properties/get-hotel-photos", headers=headers, params=querystring)
    data = json.loads(url.text)

    media_list = list()
    for i_elem in range(5):
        media_list.append(types.InputMediaPhoto(data["hotelImages"][i_elem]["baseUrl"].format(size="z")))
    return media_list

# distance = parsing_for_distance(list_with_data[2]).replace(',', '.')


def get_time():
    date = datetime.datetime.now()
    correct_date = date.strftime("Дата: %d/%m/%Y время: %H:%M:%S")
    return correct_date
