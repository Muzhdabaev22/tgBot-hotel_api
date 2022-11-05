from telebot import types
from database.classes import class_history
from database.setting import bot
from utils_directory.utils import get_time
from database.logging import logger


def highprice(message):
    """
    Команда для начала поиска самых дорогих отелей
    """
    logger.info(f'Функция {highprice.__name__} вызвана с параметром: {message}')
    class_history.setter_command_and_time(message.text, get_time())
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton('en_EN', callback_data='locate_high_en_EN'))
    kb.add(types.InlineKeyboardButton('ru_RU', callback_data='locate_high_ru_RU'))
    bot.send_message(message.from_user.id, 'Для начала выбери место действия: ',
                     reply_markup=kb)


def register_handler_highprice():
    bot.register_message_handler(highprice, commands=["highprice"])