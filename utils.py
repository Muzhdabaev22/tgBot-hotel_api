import json
import requests
from setting import headers
from bs4 import BeautifulSoup


def locations_v2_search(city):
    """
    Получаем информацию о отелях в городе
    """
    querystring = {"query": city}
    url = requests.get("https://hotels4.p.rapidapi.com/locations/v2/search/", headers=headers, params=querystring)
    data = json.loads(url.text)

    return data


def get_details_about_hotels(id_hotel):
    """
    Получение информации в виде списка [название, цена, id]
    """
    querystring = {"id": id_hotel}

    url = requests.get("https://hotels4.p.rapidapi.com/properties/get-details", headers=headers, params=querystring)

    data_json = json.loads(url.text)

    try:
        name = data_json["data"]["body"]["propertyDescription"]["name"]
        price = data_json["data"]["body"]["propertyDescription"]["featuredPrice"]["currentPrice"]["formatted"]
        result = [name, price, id_hotel]
    except Exception:
        name = data_json["data"]["body"]["propertyDescription"]["name"]
        price = "Информация отсутствует"
        result = [name, price, id_hotel]
    return result


def create_list(hotels_data_id):
    """
    Делает список из списков с отелями
    """
    list_info_about_hotel = list()
    for i in range(0, len(hotels_data_id["suggestions"][1]["entities"])):
        list_info_about_hotel.append(get_details_about_hotels(
            hotels_data_id["suggestions"][1]["entities"][i]["destinationId"]))
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


def get_image(id_hotel):
    """
    Функция для получения фотографии
    """
    querystring = {"id": id_hotel}

    url = requests.get("https://hotels4.p.rapidapi.com/properties/get-hotel-photos", headers=headers, params=querystring)
    data = json.loads(url.text)

    return data["hotelImages"][0]["baseUrl"]


def parsing_for_distance(id_hotel):
    """
    Парсинг/получение информации о расстоянии с сайта
    """
    r = requests.get(f'https://www.hotels.com/ho{id_hotel}')
    soup = BeautifulSoup(r.text, 'html.parser')
    list_soup = soup.find('ul', class_="_2sHYiJ").find_all('li')
    text = list_soup[-1].text
    return text.split(' ')[-2]


def hotel_check(list_with_data, price, distance_user):
    """
    Проверка отеля по требованиям пользователя
    """
    distance = parsing_for_distance(list_with_data[2]).replace(',', '.')
    try:
        if float(distance_user[0]) < float(distance) < float(distance_user[1]):
            if int(price[0]) < int(list_with_data[1].split('$')[-1]) < int(price[1]):
                return list_with_data
            elif list_with_data[1] == 'Информация отсутствует':
                return list_with_data
            else:
                return None
        else:
            return None
    except Exception:
        return None


def search_for_suitablel_bestdeal(list_for_sort, price, distanse):
    """
    Добавление в список подходящих отелей по цене и расстоянию до центра
    """
    ready_list = list()
    for i_hotel in range(len(list_for_sort)):
        if hotel_check(list_for_sort[i_hotel], price, distanse) is None:
            continue
        else:
            ready_list.append(hotel_check(list_for_sort[i_hotel], price, distanse))

    return ready_list
