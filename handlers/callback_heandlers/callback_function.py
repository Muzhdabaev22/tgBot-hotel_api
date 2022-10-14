from database.setting import bot
from utils_directory.utils import get_image
import database.setting as locale
from utils_directory.for_continue_utils import for_continue_lowprice_with_CITYGROUP


def image(call):
    """
    Вывод фотографий на экран
    """
    link = get_image(call.data.split('_')[-1])
    bot.send_photo(call.from_user.id, link.format(size='z'))


def locate(call):
    if call.data == "locate_en_EN":
        locale.locale_setting = "en_EN"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Место действия установлено: en_EN. Теперь введите команду "
                                   "/help для просмотра списка команд.", reply_markup=None)

    elif call.data == "locate_ru_RU":
        locale.locale_setting = "ru_RU"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Место действия установлено: ru_RU. Теперь введите команду "
                                   "/help для просмотра списка команд.", reply_markup=None)


def city_group(call):  # <<<< ЗДЕСЬ ПРОБЛЕМКА
    if call.data == "":
        bot.register_next_step_handler(call, for_continue_lowprice_with_CITYGROUP)


def register_handlers():
    bot.register_callback_query_handler(image, func=lambda call: call.data.startswith('hotel_'))
    bot.register_callback_query_handler(city_group, func=lambda call: call.data.startswith('city_group_'))
    bot.register_callback_query_handler(locate, func=lambda call: call.data.startswith('locate_'))
