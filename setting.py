import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
