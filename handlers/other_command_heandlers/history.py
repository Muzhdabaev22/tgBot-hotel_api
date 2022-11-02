from database.setting import bot
from database.classes import class_history
from utils_directory.utils import get_time


def history(message):
    class_history.setter_for_not_hotels(message.text, get_time())
    history_list = class_history.getter_history()
    try:
        for i_history in range(len(history_list)):
            if len(history_list[i_history]) == 3:
                command, time, hotels = history_list[i_history][0], history_list[i_history][1], history_list[i_history][
                    2]
                bot.send_message(message.from_user.id, f"Команда: {command},\n"
                                                       f"Дата и время: {time}\n"
                                                       f"Выведенные отели: {str(hotels)[1:-1]}")
            else:
                command, time = history_list[i_history][0], history_list[i_history][1]
                bot.send_message(message.from_user.id, f"Команда: {command},\n"
                                                       f"Дата и время: {time}\n")
    except TypeError:
        bot.send_message(message.from_user.id, "Ранее вы ничего не вводили")


def register_heandler_history():
    bot.register_message_handler(history, commands=["history"])