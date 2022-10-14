from telebot import types
from database.setting import bot
from database.classes import class_history
from utils_directory.utils import get_time


def start(message):
    """
    Хендлер для начала работы бота
    """
    class_history.setter_for_not_hotels(message.text, get_time())
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton('en_EN', callback_data='locate_en_EN'))
    kb.add(types.InlineKeyboardButton('ru_RU', callback_data='locate_ru_RU'))
    bot.send_message(message.from_user.id, "Привет! Это бот по поиску отелей. Помогу найти самый подходящий для вас "
                                           "отель!")
    bot.send_message(message.from_user.id, 'Для начала выбери место действия: ',
                     reply_markup=kb)


def register_handlers_start():
    bot.register_message_handler(start, commands=["start"])
