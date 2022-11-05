from database.setting import bot
from handlers.default_command_heandlers import help, start
from handlers.other_command_heandlers import lowprice, highprice, bestdeal, history
from handlers.callback_heandlers import callback_function
from database.logging import logger


start.register_handlers_start()
help.register_handlers_help()
lowprice.register_handlers_lowprice()
highprice.register_handler_highprice()
callback_function.register_handlers()
bestdeal.register_heandler_bestdeal()
history.register_heandler_history()


if __name__ == '__main__':
    logger.info("Бот запущен")
    bot.polling(none_stop=True)  # python main.py
