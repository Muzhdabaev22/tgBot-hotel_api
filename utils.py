import json
import os
from dotenv import load_dotenv
import requests


load_dotenv()
API_KEY = os.getenv("API_KEY")


def locations_v2_search(city):
    querystring = {"query": city}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    url = requests.get("https://hotels4.p.rapidapi.com/locations/v2/search/", headers=headers, params=querystring)
    data = json.loads(url.text)

    return data


def get_details_about_hotels(id_hotel):

    url = "https://hotels4.p.rapidapi.com/properties/get-details"

    querystring = {"id": id_hotel}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    url = requests.get("https://hotels4.p.rapidapi.com/properties/get-details", headers=headers, params=querystring)

    data_json = json.loads(url.text)

    try:
        name = data_json["data"]["body"]["propertyDescription"]["name"]
        price = data_json["data"]["body"]["propertyDescription"]["featuredPrice"]["currentPrice"]["formatted"]
        result = [name, price, id_hotel]
    except Exception:
        return None
    return result


def create_list_lowPrice(hotels_data_id):
    list_info_about_hotel = list()
    for i in range(len(hotels_data_id["suggestions"][1]["entities"])):
        if get_details_about_hotels(hotels_data_id["suggestions"][1]["entities"][i]["destinationId"]) is None:
            continue
        else:
            list_info_about_hotel.append(get_details_about_hotels(
                hotels_data_id["suggestions"][1]["entities"][i]["destinationId"]))
    return list_info_about_hotel


def sorted_lowPrice_list(dict_info):
    sorted_list = sorted(dict_info, key=lambda x: x[1])
    return sorted_list

