from database.setting import bot
from database.classes import class_history
from utils_directory.utils import get_time


@bot.message_handler(commands=['start'])
def start(message):
    """
    Хендлер для начала работы бота
    """
    class_history.setter_for_not_hotels(message.text, get_time())
    bot.send_message(message.from_user.id, 'Привет! Введи команду /help для просмотра списка команд')
