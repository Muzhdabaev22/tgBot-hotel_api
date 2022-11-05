import datetime
import json
import requests
from telebot import types
from database.setting import headers


def locations_v2_search(city, locale):
    """
    Получаем информацию об отелях в городе
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


def properties_listBESTDEAL(place, locale, price):
    querystring = {"destinationId": place, "pageNumber": "1", "pageSize": "25", "checkIn": "2022-11-19",
                   "checkOut": "2022-11-22", "adults1": "1", "priceMin": price[0], "priceMax": price[1],
                   "sortOrder": "PRICE", "locale": locale, "currency": "USD"}

    url = requests.get("https://hotels4.p.rapidapi.com/properties/list", headers=headers, params=querystring)
    data_list = json.loads(url.text)
    return data_list


def checking_suitable(place, locale, price, distance):
    data = properties_listBESTDEAL(place, locale, price)
    list_hotel = list()
    if len(data["data"]["body"]["searchResults"]["results"]) != 0:
        for i_elem in range(len(data["data"]["body"]["searchResults"]["results"])):
            distance_hotel = data["data"]["body"]["searchResults"]["results"][i_elem]["landmarks"][0]["distance"]
            if distance[0] <= distance_hotel <= distance[1]:
                list_hotel.append(add_in_list_bestdeal(data, i_elem, distance_hotel))
        return list_hotel
    else:
        return list_hotel


def add_in_list_bestdeal(data, level, distance):
    name = data["data"]["body"]["searchResults"]["results"][level]["name"]
    price = data["data"]["body"]["searchResults"]["results"][level]["ratePlan"]["price"]["current"]
    id_hotel = data["data"]["body"]["searchResults"]["results"][level]["id"]
    address = data["data"]["body"]["searchResults"]["results"][level]["address"]["streetAddress"]
    result = [name, price, id_hotel, address, distance]
    return result


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

    url = requests.get("https://hotels4.p.rapidapi.com/properties/get-hotel-photos", headers=headers,
                       params=querystring)
    data = json.loads(url.text)

    media_list = list()
    media_list.append(types.InputMediaPhoto(data["hotelImages"][0]["baseUrl"].format(size="z")))
    media_list.append(types.InputMediaPhoto(data["hotelImages"][1]["baseUrl"].format(size="z")))
    media_list.append(types.InputMediaPhoto(data["hotelImages"][2]["baseUrl"].format(size="z")))
    media_list.append(types.InputMediaPhoto(data["hotelImages"][3]["baseUrl"].format(size="z")))
    media_list.append(types.InputMediaPhoto(data["hotelImages"][4]["baseUrl"].format(size="z")))
    return media_list


def get_time():
    date = datetime.datetime.now()
    correct_date = date.strftime("Дата: %d/%m/%Y время: %H:%M:%S")
    return correct_date
