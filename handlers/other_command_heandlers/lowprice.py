from telebot import types
from database.setting import bot
from database.classes import class_history
from utils_directory.utils import get_time


def lowprice(message):
    """
    Команда для начала поиска самых дешёвых отелей
    """
    class_history.setter_command_and_time(message.text, get_time())
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton('en_EN', callback_data='locate_low_en_EN'))
    kb.add(types.InlineKeyboardButton('ru_RU', callback_data='locate_low_ru_RU'))
    bot.send_message(message.from_user.id, 'Для начала выбери место действия: ',
                     reply_markup=kb)


def register_handlers_lowprice():
    bot.register_message_handler(lowprice, commands=["lowprice"])