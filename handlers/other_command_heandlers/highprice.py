from database.classes import class_history
from database.setting import bot
from utils_directory.for_continue_utils import high_price_hotels
from utils_directory.utils import get_time


# @bot.message_handler(commands=['highprice'])
def highprice(message):
    """
    Команда для начала поиска самых дорогих отелей
    """
    class_history.setter_command_and_time(message.text, get_time())
    bot.send_message(message.from_user.id, 'Введите город')
    bot.register_next_step_handler(message, high_price_hotels)


def register_handler_highprice():
    bot.register_message_handler(highprice, commands=["highprice"])