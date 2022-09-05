import re

from loader import bot
from database.structure import Data_request_state, Users_State
from telebot.types import Message
from interface.messages import INCORRECT_LOW_PRICE_FORMAT, SELECT_HIGH_PRICE, INCORRECT_HIGH_PRICE_FORMAT, \
    INCORRECT_HIGH_PRICE_DATA, SELECT_LOW_DIST, INCORRECT_LOW_DIST_FORMAT, SELECT_HIGH_DIST, INCORRECT_HIGH_DIST_FORMAT, \
    SELECT_CHECK_IN, INCORRECT_HIGH_DIST_DATA


@bot.message_handler(state=Data_request_state.low_price)
def low_price_handler(message: Message) -> None:
    lang, curr = Users_State.state_get(user_id=message.from_user.id, key=('lang', 'curr'))
    if message.text.isdigit():
        Users_State.state_record(user_id=message.from_user.id, key='low_price', value=int(message.text))
        bot.set_state(user_id=message.from_user.id, state=Data_request_state.high_price)
        bot.send_message(chat_id=message.from_user.id, text=SELECT_HIGH_PRICE[lang].format(curr))
    else:
        bot.send_message(chat_id=message.from_user.id, text=INCORRECT_LOW_PRICE_FORMAT[lang].format(curr))


@bot.message_handler(state=Data_request_state.high_price)
def low_price_handler(message: Message) -> None:
    lang, curr, low_price = Users_State.state_get(user_id=message.from_user.id, key=('lang', 'curr', 'low_price'))
    if message.text.isdigit():
        high_price = int(message.text)
        if high_price < low_price:
            bot.send_message(chat_id=message.from_user.id, text=INCORRECT_HIGH_PRICE_DATA[lang].format(curr))

        Users_State.state_record(user_id=message.from_user.id, key='high_price', value=int(message.text))
        bot.set_state(user_id=message.from_user.id, state=Data_request_state.low_dist)
        bot.send_message(chat_id=message.from_user.id, text=SELECT_LOW_DIST[lang])
    else:
        bot.send_message(chat_id=message.from_user.id, text=INCORRECT_HIGH_PRICE_FORMAT[lang].format(curr))


@bot.message_handler(state=Data_request_state.low_dist)
def low_dist_handler(message: Message) -> None:
    lang = Users_State.state_get(user_id=message.from_user.id, key='lang')
    try:
        low_dist = float(message.text)
    except ValueError:
        bot.send_message(chat_id=message.from_user.id, text=INCORRECT_LOW_DIST_FORMAT[lang])
    else:
        Users_State.state_record(user_id=message.from_user.id, key='low_dist', value=low_dist)
        bot.set_state(user_id=message.from_user.id, state=Data_request_state.high_dist)
        bot.send_message(chat_id=message.from_user.id, text=SELECT_HIGH_DIST[lang])


@bot.message_handler(state=Data_request_state.high_dist)
def high_dist_handler(message: Message) -> None:
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


def best_deal_select(hotel_list: dict, user_id: int):
    result = []
    low_dist, high_dist = Users_State.state_get(user_id=user_id, key=('low_dist', 'high_dist'))
    for hotel in hotel_list:
        distance = re.sub(r'[\D+]', '', hotel['landmarks'][0]['distance'])
        if low_dist <= int(distance) <= high_dist:
            result.append(hotel)
    return result
