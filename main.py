# from database.setting import bot
from states.loader import bot
from utils_directory.set_bot_commands import set_default_commands

if __name__ == '__main__':
    set_default_commands(bot)
    bot.polling(none_stop=True)  # python main.py

