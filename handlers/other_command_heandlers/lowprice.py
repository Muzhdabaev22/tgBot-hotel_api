from database.setting import bot
from database.classes import class_history
from utils_directory.utils import get_time
from utils_directory.for_continue_utils import low_price_hotels


@bot.message_handler(commands=['lowprice'])
def lowprice_command(message):
    """
    Команда для начала поиска самых дешёвых отелей
    """
    class_history.setter_command_and_time(message.text, get_time())
    bot.send_message(message.from_user.id, 'Введите город')
    bot.register_next_step_handler(message, low_price_hotels)
