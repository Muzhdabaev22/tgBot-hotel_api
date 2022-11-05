from database.setting import bot
from database.classes import class_history
from utils_directory.utils import get_time
from database.logging import logger


def help_command(message):
    """
    Команда для вывода всех функций
    """
    logger.info(f'Функция {help_command.__name__} вызвана с параметром: {message}')
    class_history.setter_for_not_hotels(message.text, get_time())
    bot.send_message(message.from_user.id, 'Список команд: \n'
                                           '● /lowprice — вывод самых дешёвых отелей в городе,\n'
                                           '● /highprice — вывод самых дорогих отелей в городе,\n'
                                           '● /bestdeal — вывод отелей, наиболее подходящих по цене и расположению '
                                           'от центра,\n '
                                           '● /history — вывод истории поиска отелей.')


def register_handlers_help():
    bot.register_message_handler(help_command, commands=["help"])