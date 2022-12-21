"""
Сценарий обработки команды bestdeal
"""
from loader import bot, logger
from database.structure import Data_request_state, Users_State
from telebot.types import Message
from interface.messages import INCORRECT_LOW_PRICE_FORMAT, SELECT_HIGH_PRICE, INCORRECT_HIGH_PRICE_FORMAT, \
    INCORRECT_HIGH_PRICE_DATA, SELECT_LOW_DIST, INCORRECT_LOW_DIST_FORMAT, SELECT_HIGH_DIST, INCORRECT_HIGH_DIST_FORMAT, \
    SELECT_CHECK_IN, INCORRECT_HIGH_DIST_DATA


@logger.catch
@bot.message_handler(state=Data_request_state.low_price)
def low_price_handler(message: Message) -> None:
    """
    Шаг 4а:
    Хэндлер-обработчик нижней границы стоимости.
    После выбора нижней границы стоимости, записывает результат в стейт пользователя.
    Затем устанавливает стейт high_price и ждет верхней границы стоимости.
    :param message: Message
    """
    lang = Users_State.state_get(user_id=message.from_user.id, key='lang')
    if message.text.isdigit():
        Users_State.state_record(user_id=message.from_user.id, key='low_price', value=int(message.text))
        bot.set_state(user_id=message.from_user.id, state=Data_request_state.high_price)
        bot.send_message(chat_id=message.from_user.id, text=SELECT_HIGH_PRICE[lang])
    else:
        bot.send_message(chat_id=message.from_user.id, text=INCORRECT_LOW_PRICE_FORMAT[lang])


@logger.catch
@bot.message_handler(state=Data_request_state.high_price)
def high_price_handler(message: Message) -> None:
    """
    Шаг 4б:
    Хэндлер-обработчик верхней границы стоимости.
    После ввода верхней границы стоимости проверяет вводимую информацию (нижняя граница должна
    быть меньше верхней границы), записывает результат в стейт пользователя.
    Затем устанавливает стейт low_dist и ждет нижней границы расстояния.
    :param message: Message
    """

    lang, low_price = Users_State.state_get(user_id=message.from_user.id, key=('lang', 'low_price'))
    if message.text.isdigit():
        high_price = int(message.text)
        if high_price < low_price:
            bot.send_message(chat_id=message.from_user.id, text=INCORRECT_HIGH_PRICE_DATA[lang])

        Users_State.state_record(user_id=message.from_user.id, key='high_price', value=int(message.text))
        bot.set_state(user_id=message.from_user.id, state=Data_request_state.low_dist)
        bot.send_message(chat_id=message.from_user.id, text=SELECT_LOW_DIST[lang])
    else:
        bot.send_message(chat_id=message.from_user.id, text=INCORRECT_HIGH_PRICE_FORMAT[lang])


@logger.catch
@bot.message_handler(state=Data_request_state.low_dist)
def low_dist_handler(message: Message) -> None:
    """
    Шаг 4в:
    Хэндлер-обработчик ижней границы расстояния.
    После ввода нижней границы расстояния от центра города, записывает результат в стейт пользователя.
    Затем устанавливает стейт high_dist и ждет верхней границы расстояния.
    :param message: Message
    """
    lang = Users_State.state_get(user_id=message.from_user.id, key='lang')
    try:
        low_dist = float(message.text)
    except ValueError:
        bot.send_message(chat_id=message.from_user.id, text=INCORRECT_LOW_DIST_FORMAT[lang])
    else:
        Users_State.state_record(user_id=message.from_user.id, key='low_dist', value=low_dist)
        bot.set_state(user_id=message.from_user.id, state=Data_request_state.high_dist)
        bot.send_message(chat_id=message.from_user.id, text=SELECT_HIGH_DIST[lang])


@logger.catch
@bot.message_handler(state=Data_request_state.high_dist)
def high_dist_handler(message: Message) -> None:
    """
    Шаг 4г:
    Хэндлер-обработчик верхней границы расстояния.
    После ввода верхней границы расстояния от центра города, проверяет вводимую информацию (нижняя граница должна
    быть меньше верхней границы), записывает результат в стейт пользователя.
    Затем устанавливает стейт check_in.
    :param message: Message
    """
    lang, low_dist = Users_State.state_get(user_id=message.from_user.id, key=('lang', 'low_dist'))
    try:
        high_dist = float(message.text)
    except ValueError:
        bot.send_message(chat_id=message.from_user.id, text=INCORRECT_HIGH_DIST_FORMAT[lang])
    else:
        if low_dist > high_dist:
            bot.send_message(chat_id=message.from_user.id, text=INCORRECT_HIGH_DIST_DATA[lang])
        else:
            Users_State.state_record(user_id=message.from_user.id, key='high_dist', value=high_dist)
            bot.set_state(user_id=message.from_user.id, state=Data_request_state.check_in)
            bot.send_message(chat_id=message.from_user.id, text=SELECT_CHECK_IN[lang])


@logger.catch
def best_deal_select(hotel_list: list[dict], user_id: int) -> list:
    """
    Функиця отбора из списка отелей только тех, которые удовлетворяют требованиям расстояни от центра.
    :param hotel_list: list[dict] - список проверяемых отелей
    :param user_id: int - id пользователя в телеграм

    :return result: list - список подходящих по требованиям отелей
    """

    result = []
    low_dist, high_dist = Users_State.state_get(user_id=user_id, key=('low_dist', 'high_dist'))
    for hotel in hotel_list:
        distance = hotel["destinationInfo"]["distanceFromDestination"]["value"]
        if low_dist <= int(distance) <= high_dist:
            result.append(hotel)
    return result
