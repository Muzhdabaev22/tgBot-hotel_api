import telebot
from config import API_KEY, TOKEN

bot = telebot.TeleBot(TOKEN)

locale_setting = "en_EN"

headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
