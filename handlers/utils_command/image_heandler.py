from database.setting import bot
from utils_directory.utils import get_image


@bot.callback_query_handler(func=lambda call: call.data.startswith('hotel_'))
def image(call):
    """
    Вывод фотографий на экран
    """
    link = get_image(call.data.split('_')[-1])
    bot.send_photo(call.from_user.id, link.format(size='z'))