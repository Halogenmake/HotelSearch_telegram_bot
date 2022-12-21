"""
Сценарий команы history.
"""

from loader import bot, logger
from telebot.types import CallbackQuery

from interface.messages import HISTORY_SELECT, HISTORY_SHOW_MESSAGE
from keyboards.keyboards import show_history_keys

from handlers.lowprice_higthprice import media_massive_maker, abort_command

from database.structure import DataBase


@logger.catch
def history_select(user_id: int) -> None:
    """
    Функция, отправляющая сообщение с кнопками работы с историей.
    :param user_id: int - id пользователя в телеграме
    """
    lang = DataBase.user_get_lang(user_id=user_id)
    bot.send_message(chat_id=user_id, text=HISTORY_SELECT[lang], reply_markup=show_history_keys(lang))


@logger.catch
@bot.callback_query_handler(func=lambda call: call.data in ['last3', 'all'])
def history_show(call: CallbackQuery) -> None:
    """
    Хэндлер, реагирующий на нажатие кнопок работы с историей.
    Осуществляет первичный запрос к таблице БД, содержащей запросы пользовтелей, затем в цикле
    по каждому из полученных запросов забирает из БД данные о найденых отелях и выводит их в виде сообщений в телеграмм.
    Выводит или три последних запроса, или все запросы пользователя от последнего до первого
    :param call: CallbackQuery
    """


    lang = DataBase.user_get_lang(user_id=call.from_user.id)
    limit = 3
    if call.data == 'all':
        limit = -1

    requests = DataBase.history_requests_get(user_id=call.from_user.id, limit=limit)
    for i_requests in requests:
        request_id, content, date = i_requests
        bot.send_message(chat_id=call.from_user.id, text='\n'.join((HISTORY_SHOW_MESSAGE[lang].format(date), content)), parse_mode='html')
        hotel_list = DataBase.history_hotels_get(request_id=request_id)
        for i_hotel in hotel_list:
            content, photo_list = i_hotel
            if not photo_list:
                bot.send_message(chat_id=call.from_user.id, text=content, parse_mode='html')
            else:
                photo_list.split(sep='\n')
                bot.send_media_group(chat_id=call.from_user.id, media=media_massive_maker(photo_list=photo_list.split(sep='\n'), caption=content))
    else:
        abort_command(user_id=call.from_user.id, lang=lang)
