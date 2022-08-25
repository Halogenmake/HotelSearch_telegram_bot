"""
Пакет содержит хэндлеры основного меню бота
"""

from telebot.types import Message, CallbackQuery
from telebot.apihelper import ApiTelegramException

from loader import bot
from interface.messages import SELECT_LANG, DEFAULT_COMMANDS, CHOICE_LANG
from keyboards.keyboards import select_lang_key, main_menu_keys
from database.structure import DataBase
from keyboards.key_text import EN_CALL, RU_CALL, SET_LANG_CALL, LOWPRICE_CALL, HIGHPRICE_CALL, BESTDEAL_CALL, \
    HISTORY_CALL
from handlers.lowprice_higthprice import lowprice_higthprice_start


def clear_inline_keyboard(message: Message) -> None:
    """
    Функция удаляет главное меню, если была выбрана какая-либо команда
    :param message: Message
    """
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except ApiTelegramException:
        pass
    except AttributeError:
        pass


def main_menu(lang: str, user_id: int) -> None:
    """
    Вспомогательная функция, возвращающая главное меню бота
    :param lang: str - язык интерфейса пользователя
    :param user_id: int id прользователя в телеграме
    """
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS[lang].items()]
    bot.send_message(user_id, '\n'.join(text), reply_markup=main_menu_keys(lang))


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Хендлер комманды /start. Если записи пользователя нет в БД, то предлагает выбрать язык интерфейса,
    если есть, то выводит подсказку и главное меню
    :param message: Message
    :return:
    """
    if not DataBase.user_set(message.from_user.id):
        bot.send_message(message.from_user.id, SELECT_LANG, reply_markup=select_lang_key)
    else:
        bot_help(message)


@bot.message_handler(commands=[SET_LANG_CALL])
def select_lang_reply(message: Message) -> None:
    """
    Хэндлер команды /set_lang. Выдает сообщение с клавиатурой выбора языка
    :param message:
    :return:
    """
    bot.send_message(message.from_user.id, SELECT_LANG, reply_markup=select_lang_key)


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """
    Хэндлек команды /help. Выдает главное меню бота в зависимости от языковых настроек
    :param message: Message
    """
    lang = DataBase.user_get_lang(user_id=message.from_user.id)
    main_menu(lang=lang, user_id=message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data in [EN_CALL, RU_CALL, SET_LANG_CALL])
def select_lang_inline(call: CallbackQuery) -> None:
    """
    Хэндлер обработки инлайн-кнопок выбора языка.
    После выбора языка интерфейса - записывает данные в БД.
    :param call:
    :return:
    """

    if call.data == SET_LANG_CALL:
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=SELECT_LANG, reply_markup=select_lang_key
        )
    else:
        DataBase.user_set_lang(lang=call.data, user_id=call.from_user.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=CHOICE_LANG[call.data]
        )
        main_menu(lang=call.data, user_id=call.from_user.id)


@bot.message_handler(commands=[LOWPRICE_CALL, HIGHPRICE_CALL, BESTDEAL_CALL, HISTORY_CALL])
def command_forward_reply(message: Message) -> None:
    """
    Хэндлер команд /lowprice, /highprice, /bestdeal, /history.
    Перенаправляет в соответсвующий сценарий
    :param message: Message
    """
    clear_inline_keyboard(message)
    if message.text == '/' + LOWPRICE_CALL or message.text == '/' + HIGHPRICE_CALL:
        lowprice_higthprice_start(user_id=message.from_user.id, command=message.text[1:])


@bot.callback_query_handler(func=lambda call: call.data in [LOWPRICE_CALL, HIGHPRICE_CALL, BESTDEAL_CALL, HISTORY_CALL])
def command_forward_inline(call: CallbackQuery) -> None:
    """
    Хэндлер команд клавного меню бота в инлайн режиме.
    Перенаправляет в соответсвующий сценарий
    :param call: CallbackQuery
    """

    clear_inline_keyboard(call.message)
    if call.data == LOWPRICE_CALL or call.data == HIGHPRICE_CALL:
        lowprice_higthprice_start(user_id=call.from_user.id, command=call.data)
