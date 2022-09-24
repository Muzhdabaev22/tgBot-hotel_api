from database.classes import class_history
from database.setting import bot
from utils_directory.for_continue_utils import range_price
from utils_directory.utils import get_time


@bot.message_handler(commands=['bestdeal'])
def bestdeal_command(message):
    """
    Команда для начала поиска наиболее подходящих по цене и расположению от центра отеля
    """
    class_history.setter_command_and_time(message.text, get_time())
    bot.send_message(message.from_user.id, 'Введите город')
    bot.register_next_step_handler(message, range_price)
