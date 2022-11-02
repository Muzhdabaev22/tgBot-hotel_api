from database.setting import bot
from utils_directory.for_continue_utils import low_price_hotel, with_photo_questionLOW, high_price_hotels, \
    with_photo_questionHIGH, best_deal_hotel, with_photo_questionBEST


def locate_low_price(call):
    if call.data == 'locate_low_en_EN':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Место действия установлено: en_EN. Теперь введите город, где хотите найти отель.",
                              reply_markup=None)
        bot.register_next_step_handler(call.message, low_price_hotel, "en_EN")

    elif call.data == "locate_low_en_EN":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Место действия установлено: ru_RU. Теперь введите город, где хотите найти отель.",
                              reply_markup=None)
        bot.register_next_step_handler(call.message, low_price_hotel, "ru_RU")


def locate_high_price(call):
    if call.data == "locate_high_en_EN":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Место действия установлено: en_EN. Теперь введите город, где хотите найти отель.",
                              reply_markup=None)
        bot.register_next_step_handler(call.message, high_price_hotels, "en_EN")

    elif call.data == "locate_high_en_EN":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Место действия установлено: ru_RU. Теперь введите город, где хотите найти отель.",
                              reply_markup=None)
        bot.register_next_step_handler(call.message, high_price_hotels, "ru_RU")


def locate_bestdeal(call):
    if call.data == "locate_best_en_EN":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Место действия установлено: en_EN. Теперь введите город, где хотите найти отель.",
                              reply_markup=None)
        bot.register_next_step_handler(call.message, best_deal_hotel, "en_EN")

    elif call.data == "locate_best_en_EN":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Место действия установлено: ru_RU. Теперь введите город, где хотите найти отель.",
                              reply_markup=None)
        bot.register_next_step_handler(call.message, best_deal_hotel, "ru_RU")


def city_groupLOW(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Вам выводить отели с фотографиями или без?(Да/Нет)", reply_markup=None)
    bot.register_next_step_handler(call.message, with_photo_questionLOW, call.data.split("_")[1], call.data.split("_")[2])


def city_groupHIGH(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Вам выводить отели с фотографиями или без?(Да/Нет)", reply_markup=None)
    bot.register_next_step_handler(call.message, with_photo_questionHIGH, call.data.split("_")[1], call.data.split("_")[2])


def city_groupBEST(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Вам выводить отели с фотографиями или без?(Да/Нет)", reply_markup=None)
    bot.register_next_step_handler(call.message, with_photo_questionBEST, call.data.split("_")[1], call.data.split("_")[2])


def register_handlers():
    bot.register_callback_query_handler(city_groupLOW, func=lambda call: call.data.startswith('citygroupLOW_'))
    bot.register_callback_query_handler(city_groupHIGH, func=lambda call: call.data.startswith('citygroupHIGH_'))
    bot.register_callback_query_handler(city_groupBEST, func=lambda call: call.data.startswith('citygroupBEST_'))
    bot.register_callback_query_handler(locate_low_price, func=lambda call: call.data.startswith('locate_low'))
    bot.register_callback_query_handler(locate_high_price, func=lambda call: call.data.startswith('locate_high'))
    bot.register_callback_query_handler(locate_bestdeal, func=lambda call: call.data.startswith('locate_best'))