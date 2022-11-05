from database.logging import logger
from database.setting import bot
from database.classes import class_history
from utils_directory.utils import get_time


def start(message):
    """
    Хендлер для начала работы бота
    """
    logger.info(f'Функция {start.__name__} вызвана с параметром: {message}')
    class_history.setter_for_not_hotels(message.text, get_time())
    bot.send_message(message.from_user.id, "Привет! Это бот по поиску отелей. Помогу найти самый подходящий для вас "
                                           "отель! \nДля просмотра команд введи команду /help")


def register_handlers_start():
    bot.register_message_handler(start, commands=["start"])
