import requests
import json

city = 'moscow'
count_hotels = ''

querystring = {"query": f"{city}", "currency": "USD"}

headers = {
    "X-RapidAPI-Key": "877e7262b9msh80be8ffb3287018p105eacjsnee4a1c0cd717",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

url = requests.get("https://hotels4.p.rapidapi.com/locations/v2/search/", headers=headers, params=querystring)


def write_json(data: requests, name_file):
    data = json.loads(data.text)
    with open(f'{name_file}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


write_json(url, "data")


data_check = json.loads(url.text)

if data_check['moresuggestions'] == 0:
    print('Отелей в этом городе нет или этого города не существует.')
else:
    print(f'Найдены предложения: {data_check["moresuggestions"]}')

