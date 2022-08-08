import requests
import json

my_req = requests.get('https://rapidapi.com/apidojo/api/hotels4/')

data = json.loads(my_req.text)

with open('data_hotels.json', 'w') as file:
	json.dump(data, file, indent=4)



