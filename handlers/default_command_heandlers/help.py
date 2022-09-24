from database.setting import bot
from database.classes import class_history
from utils_directory.utils import get_time


@bot.message_handler(commands=['help'])
def help_command(message):
    """
    Команда для вывода всех функций
    """
    class_history.setter_for_not_hotels(message.text, get_time())
    bot.send_message(message.from_user.id, 'Список команд: \n'
                                           '● /lowprice — вывод самых дешёвых отелей в городе,\n'
                                           '● /highprice — вывод самых дорогих отелей в городе,\n'
                                           '● /bestdeal — вывод отелей, наиболее подходящих по цене и расположению '
                                           'от центра,\n '
                                           '● /history — вывод истории поиска отелей.')
