from typing import Any, Union
import re
import datetime

from telebot.types import Message, CallbackQuery
from config_data.API_requests import request_city_search

import handlers

from loader import bot
from database.structure import Data_request_state, DataBase
from interface.messages import LOWPRICE_STAE, HIGHPRICE_STATE, SELECT_CITY, \
    INCORRECT_CITY, CORRECT_CITY, ERROR_CITY, CHOICE_CITY, SELECT_CURRENCY, CHOICE_CURRENCY, \
    SELECT_COUNT_HOTEL, CHOICE_COUNT_HOTEL, SELECT_CHECK_IN, INCORRECT_CHECK_IN_FORMAT, INCORRECT_CHECK_IN_DATA, \
    SELECT_CHECK_OUT, INCORRECT_CHECK_OUT_FORMAT, INCORRECT_CHECK_OUT_DATA, SELECT_LOAD_PHOTO, SELECT_COUNT_PHOTO,\
    REQUEST_CARD
from keyboards.key_text import LOWPRICE_CALL, CURRENCY_KEY_CALL, COUNT_HOTEL_CALL, COUNT_PHOTO_CALL, HIGHPRICE_CALL
from keyboards.keyboards import city_corr_keys, currency_keys, hotels_count_keys, select_photo_keys


def state_record(user_id: int, key: Union[tuple, Any], value: Union[tuple, Any]) -> None:
    with bot.retrieve_data(user_id=user_id) as data:
        if not isinstance(key, tuple) or not isinstance(value, tuple):
            data[key] = value
        else:
            for i_key, i_value in zip(key, value):
                data[i_key] = i_value


def state_get(user_id: int, key: str) -> Any:
    with bot.retrieve_data(user_id=user_id) as data:
        return data[key]


def state_print(user_id):
    with bot.retrieve_data(user_id=user_id) as data:
        print()
        for i_data in data.items():
            print(i_data)


def lowprice_higthprice_start(user_id: int, command: str) -> None:
    bot.delete_state(user_id)
    lang = DataBase.user_get_lang(user_id=user_id)
    bot.set_state(user_id, Data_request_state.city)
    state_record(user_id=user_id, key=('lang', 'command'), value=(lang, command))
    if command == LOWPRICE_CALL:
        bot.send_message(user_id, LOWPRICE_STAE[lang])
    else:
        bot.send_message(user_id, HIGHPRICE_STATE[lang])
    bot.send_message(user_id, SELECT_CITY[lang])
    state_print(user_id)


@bot.message_handler(state='*', commands=['start', 'help'])
def cancel(message: Message):
    bot.delete_state(message.from_user.id)
    handlers.start.bot_start(message)


@bot.message_handler(state=Data_request_state.city)
def search_city_handler(message: Message) -> None:
    response = request_city_search(message.text)

    if response.status_code == 200:
        pattern_city_group = r'(?<="CITY_GROUP",).+?[\]]'
        find_cities = re.findall(pattern_city_group, response.text)
        if len(find_cities[0]) > 20:
            pattern_dest = r'(?<="destinationId":")\d+'
            destination = re.findall(pattern_dest, find_cities[0])

            pattern_city = r'(?<="name":")\w+[\s, \w]\w+'
            city = re.findall(pattern_city, find_cities[0])

            city_list = list(zip(destination, city))

            bot.send_message(message.from_user.id, CORRECT_CITY[state_get(message.from_user.id, 'lang')],
                             reply_markup=city_corr_keys(city_list))

        else:
            bot.send_message(message.from_user.id, INCORRECT_CITY[state_get(message.from_user.id, 'lang')])

    else:
        bot.send_message(message.from_user.id, ERROR_CITY[state_get(message.from_user.id, 'lang')])


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def callback_city(call: CallbackQuery) -> None:
    for city in call.message.json['reply_markup']['inline_keyboard']:
        if city[0]['callback_data'] == call.data:
            state_record(call.from_user.id, ('city', 'city_id'), (city[0]['text'], call.data))
            break

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.edit_message_text(
        message_id=call.message.message_id, chat_id=call.message.chat.id,
        text=CHOICE_CITY[state_get(user_id=call.from_user.id, key='lang')].format(
            state_get(user_id=call.from_user.id, key='city'))
    )

    bot.send_message(
        call.from_user.id, SELECT_CURRENCY[state_get(user_id=call.from_user.id, key='lang')],
        reply_markup=currency_keys()
    )
    bot.set_state(call.from_user.id, Data_request_state.curr)
    state_print(call.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data in CURRENCY_KEY_CALL)
def callback_currency(call: CallbackQuery) -> None:
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=CHOICE_CURRENCY[state_get(user_id=call.from_user.id, key='lang')].format(call.data)
    )

    state_record(user_id=call.from_user.id, key='curr', value=call.data)
    state_print(call.from_user.id)
    bot.set_state(call.from_user.id, Data_request_state.hotel_count)
    bot.send_message(
        call.from_user.id, SELECT_COUNT_HOTEL[state_get(user_id=call.from_user.id, key='lang')],
        reply_markup=hotels_count_keys(COUNT_HOTEL_CALL)
    )


@bot.callback_query_handler(func=lambda call: call.data in COUNT_HOTEL_CALL.keys())
def callback_hotel_count(call: CallbackQuery) -> None:
    count_hotel = COUNT_HOTEL_CALL[call.data]
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=CHOICE_COUNT_HOTEL[state_get(user_id=call.from_user.id, key='lang')].format(str(count_hotel))
    )
    state_record(user_id=call.from_user.id, key='hotel_count', value=count_hotel)
    state_print(call.from_user.id)
    bot.set_state(call.from_user.id, Data_request_state.check_in)
    bot.send_message(
        call.from_user.id, SELECT_CHECK_IN[state_get(user_id=call.from_user.id, key='lang')]
    )


@bot.message_handler(state=Data_request_state.check_in)
def check_in_handler(message: Message) -> None:
    lang = state_get(user_id=message.from_user.id, key='lang')
    try:
        check_in_date = datetime.datetime.strptime(message.text, '%Y-%m-%d')
    except ValueError:
        bot.send_message(
            message.from_user.id, INCORRECT_CHECK_IN_FORMAT[lang],
        )
    else:
        if datetime.datetime.now() > check_in_date:
            bot.send_message(
                message.from_user.id, INCORRECT_CHECK_IN_DATA[lang],
            )
        else:
            state_record(user_id=message.from_user.id, key='check_in', value=check_in_date.date().strftime('%Y-%m-%d'))
            state_print(message.from_user.id)
            bot.set_state(message.from_user.id, Data_request_state.check_out)
            bot.send_message(
                message.from_user.id, SELECT_CHECK_OUT[lang],
            )


@bot.message_handler(state=Data_request_state.check_out)
def check_out_handler(message: Message) -> None:
    lang = state_get(user_id=message.from_user.id, key='lang')
    try:
        check_out_date = datetime.datetime.strptime(message.text, '%Y-%m-%d')
    except ValueError:
        bot.send_message(
            message.from_user.id, INCORRECT_CHECK_OUT_FORMAT[lang],
        )
    else:
        check_in_date = datetime.datetime.strptime(state_get(user_id=message.from_user.id, key='check_in'), '%Y-%m-%d')
        if check_in_date >= check_out_date:
            bot.send_message(
                message.from_user.id, INCORRECT_CHECK_OUT_DATA[lang],
            )
        else:
            state_record(user_id=message.from_user.id, key='check_out',
                         value=check_out_date.date().strftime('%Y-%m-%d'))
            state_print(message.from_user.id)
            bot.set_state(message.from_user.id, Data_request_state.check_out)
            bot.send_message(
                message.from_user.id, SELECT_LOAD_PHOTO[lang],
                reply_markup=select_photo_keys(lang=lang)

            )


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def callback_select_photo(call: CallbackQuery) -> None:
    if call.data == 'yes':
        state_record(user_id=call.from_user.id, key='photo', value=True)
        bot.edit_message_text(
            message_id=call.message.message_id, chat_id=call.message.chat.id,
            text=SELECT_COUNT_PHOTO[state_get(user_id=call.from_user.id, key='lang')], reply_markup=hotels_count_keys(COUNT_PHOTO_CALL))
    else:
        state_record(user_id=call.from_user.id, key='photo', value=False)

    state_print(call.from_user.id)
