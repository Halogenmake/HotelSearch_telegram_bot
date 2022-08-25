"""
Сценарий команд lowprice, hothprice.
"""


import re
import datetime
import json
import requests

from telebot.types import Message, CallbackQuery, InputMediaPhoto

from loader import bot
import handlers
from config_data.API_requests import request_city_search, request_hotel_search, request_get_photo
from database.structure import Data_request_state, DataBase, Users_State

from config_data.config import URL_HOTEL

from interface.messages import LOWPRICE_STAE, HIGHPRICE_STATE, SELECT_CITY, \
    INCORRECT_CITY, CORRECT_CITY, ERROR_CITY, CHOICE_CITY, SELECT_CURRENCY, CHOICE_CURRENCY, \
    SELECT_COUNT_HOTEL, CHOICE_COUNT_HOTEL, SELECT_CHECK_IN, INCORRECT_CHECK_IN_FORMAT, INCORRECT_CHECK_IN_DATA, \
    SELECT_CHECK_OUT, INCORRECT_CHECK_OUT_FORMAT, INCORRECT_CHECK_OUT_DATA, SELECT_LOAD_PHOTO, SELECT_COUNT_PHOTO, \
    CHOICE_COUNT_PHOTO, PLEASE_WHAIT, ERROR_HOTEL, DEFAULT_COMMANDS, HOTEL_TEMPLATE, NOT_FOUND, SEARCH_COMPLETE, REQUEST_CARD_TEMPLATE

from keyboards.key_text import LOWPRICE_CALL, CURRENCY_KEY_CALL, COUNT_HOTEL_CALL, COUNT_PHOTO_CALL, BESTDEAL_CALL, \
    HIGHPRICE_CALL
from keyboards.keyboards import city_corr_keys, currency_keys, hotels_count_keys, select_photo_keys, main_menu_keys


def request_card_builder(template: str, param: tuple) -> str:
    """
    Вспомогательная функция формирования итоговой карточки запроса

    :param template: str - Шаблон итоговой карточки запроса,
    :param param: tuple - Параметры, пенредаваемые в шаблон запроса,
    :return: str - Возвращает заполненную итоговую карточку запроса
    """
    text = template.format(*param)
    return text


def lowprice_higthprice_start(user_id: int, command: str) -> None:
    """
    Шаг 0:
    Начало сценария команд lowprice, hothprice.
    Сначала получает язык пользователя из БД.
    Затем устанавливает стейт выбора города
    В конце записывает в стейт пользователя параметры 'lang' и 'command' (язык и выбранная команда соответственно)

    :param user_id: int - id прользователя в телеграме
    :param command: - выбранная команда
    :return:
    """

    lang = DataBase.user_get_lang(user_id=user_id)

    bot.delete_state(user_id=user_id)
    bot.set_state(user_id=user_id, state=Data_request_state.city)

    if command == LOWPRICE_CALL:
        Users_State.state_record(user_id=user_id, key=('lang', 'command'),
                                 value=(lang, command))
    else:
        Users_State.state_record(user_id=user_id, key=('lang', 'command'),
                                 value=(lang, command))

    bot.send_message(chat_id=user_id, text=SELECT_CITY[lang])


@bot.message_handler(state='*', commands=['start', 'help'])
def cancel(message: Message) -> None:
    """
    Хэндлер-функция прерывания сценария по команде /start, /help
    :param message: Message
    """
    bot.delete_state(user_id=message.from_user.id)
    handlers.start.bot_start(message=message)


@bot.message_handler(state=Data_request_state.city)
def search_city_handler(message: Message) -> None:
    """
    Шаг 1:
    Хэндлер стейта city. После ввода города делает запрос по API для уточнения города.
    Если город не найдет - просит ввести город еще раз.
    Если найден - то выдает инлайн-клавиатуру для уточнения города.
    :param message: Message
    """

    lang = Users_State.state_get(user_id=message.from_user.id, key='lang')

    response = request_city_search(user_id=message.from_user.id, text=message.text)

    if response.status_code == 200:
        pattern_city_group = r'(?<="CITY_GROUP",).+?[\]]'
        find_cities = re.findall(pattern_city_group, response.text)
        print(find_cities)
        if len(find_cities[0]) > 20:
            pattern_dest = r'(?<="destinationId":")\d+'
            destination = re.findall(pattern_dest, find_cities[0])

            pattern_city = r'(?<="name":")\w+[\s, \w]\w+'
            city = re.findall(pattern_city, find_cities[0])

            city_list = list(zip(destination, city))

            bot.send_message(chat_id=message.from_user.id, text=CORRECT_CITY[lang],
                             reply_markup=city_corr_keys(city_list))

        else:
            bot.send_message(chat_id=message.from_user.id, text=INCORRECT_CITY[lang])

    else:
        bot.send_message(chat_id=message.from_user.id, text=ERROR_CITY[lang])


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def callback_city(call: CallbackQuery) -> None:
    """
    Шаг 2:
    Хэндлер-обработчик инлайн-клавиатуры уточнения города.
    После выбора какого-либо города записывает название города и его id в стейт пользователя.
    После чего выдает клавиатуру выбора валюты
    :param call:
    :return:
    """

    lang = Users_State.state_get(user_id=call.from_user.id, key='lang')
    city_select = ''
    for city in call.message.json['reply_markup']['inline_keyboard']:
        if city[0]['callback_data'] == call.data:
            city_select = city[0]['text']
            Users_State.state_record(user_id=call.from_user.id, key=('city', 'city_id'),
                                     value=(city_select, call.data))
            break

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.edit_message_text(
        message_id=call.message.message_id, chat_id=call.message.chat.id,
        text=CHOICE_CITY[lang].format(city_select))

    bot.send_message(
        chat_id=call.from_user.id, text=SELECT_CURRENCY[lang],
        reply_markup=currency_keys()
    )


@bot.callback_query_handler(func=lambda call: call.data in CURRENCY_KEY_CALL)
def callback_currency(call: CallbackQuery) -> None:
    """
    Шаг 3:
    Хэндлер-обработчик инлайн-клавиатуры выбора валюты. Реагирует только на CURRENCY_KEY_CALL
    После выбора валюты записывает её в стейт пользователя.
    В конце выдает клавиатуру выбора количества отображаемых отелей.
    :param call: CallbackQuery
    """

    lang = Users_State.state_get(user_id=call.from_user.id, key='lang')
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=CHOICE_CURRENCY[lang].format(call.data)
    )

    Users_State.state_record(user_id=call.from_user.id, key='curr', value=call.data)
    bot.send_message(
        chat_id=call.from_user.id, text=SELECT_COUNT_HOTEL[lang],
        reply_markup=hotels_count_keys(COUNT_HOTEL_CALL)
    )


@bot.callback_query_handler(func=lambda call: call.data in COUNT_HOTEL_CALL.keys())
def callback_hotel_count(call: CallbackQuery) -> None:
    """
    Шаг 4:
    Хэндлер-обработчик инлайн-клавиатуры выбора количества отелей. Реагирует только на COUNT_HOTEL_CALL.keys
    После выбора количества записывает результат в стейт пользователя.
    Затем устанавливает стейт check_in и ждет ввода даты заезда.
    :param call: call.data
    """
    count_hotel = COUNT_HOTEL_CALL[call.data]
    lang = Users_State.state_get(user_id=call.from_user.id, key='lang')

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=CHOICE_COUNT_HOTEL[lang].format(str(count_hotel))
    )

    Users_State.state_record(user_id=call.from_user.id, key='hotel_count', value=count_hotel)

    bot.set_state(user_id=call.from_user.id, state=Data_request_state.check_in)
    bot.send_message(
        chat_id=call.from_user.id, text=SELECT_CHECK_IN[lang]
    )


@bot.message_handler(state=Data_request_state.check_in)
def check_in_handler(message: Message) -> None:
    """
    Шаг 5:
    Хэндлер стейта check_in. осуществляет проверку ввода пользователя по двум параметрам:
    - Формат даты
    - Дата не должна быть раньше текущей.
    Если все впорядке - записываает данные в стейт пользователя и устанавливает стейт check_out
    :param message: Message
    """

    lang = Users_State.state_get(user_id=message.from_user.id, key='lang')
    try:
        check_in_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
    except ValueError:
        bot.send_message(
            chat_id=message.from_user.id, text=INCORRECT_CHECK_IN_FORMAT[lang],
        )
    else:
        if datetime.datetime.now().date() > check_in_date:
            bot.send_message(
                chat_id=message.from_user.id, text=INCORRECT_CHECK_IN_DATA[lang],
            )
        else:
            Users_State.state_record(user_id=message.from_user.id, key='check_in',
                                     value=check_in_date.strftime('%Y-%m-%d'))

            bot.set_state(user_id=message.from_user.id, state=Data_request_state.check_out)
            bot.send_message(
                chat_id=message.from_user.id, text=SELECT_CHECK_OUT[lang],
            )


@bot.message_handler(state=Data_request_state.check_out)
def check_out_handler(message: Message) -> None:
    """
    Шаг 6:
    Хэндлер стейта check_out. Осуществляет проверку ввода пользователя по двум параметрам:
    - Формат даты
    - Дата не должна быть раньше даты заезда.
    Если все впорядке - записываает данные в стейт пользователя и выдает клавиатуру на выбор необходимости загрузки фото отеля
    :param message: Message
    """

    lang, check_in = Users_State.state_get(user_id=message.from_user.id, key=('lang', 'check_in'))
    try:
        check_out_date = datetime.datetime.strptime(message.text, '%Y-%m-%d')
    except ValueError:
        bot.send_message(
            chat_id=message.from_user.id, text=INCORRECT_CHECK_OUT_FORMAT[lang],
        )
    else:
        check_in_date = datetime.datetime.strptime(check_in, '%Y-%m-%d')
        if check_in_date >= check_out_date:
            bot.send_message(
                chat_id=message.from_user.id, text=INCORRECT_CHECK_OUT_DATA[lang],
            )
        else:
            Users_State.state_record(user_id=message.from_user.id, key='check_out',
                                     value=check_out_date.date().strftime('%Y-%m-%d'))

            bot.set_state(user_id=message.from_user.id, state=Data_request_state.check_out)
            bot.send_message(
                chat_id=message.from_user.id, text=SELECT_LOAD_PHOTO[lang],
                reply_markup=select_photo_keys(lang=lang)
            )


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def callback_select_photo(call: CallbackQuery) -> None:
    """
    Шаг 7:
    Хандоер инлайн-клавиатуры необходимости загрузки фото отеля. Реагирует только на кнопки ['yes', 'no']
    - Если выбран 'yes', записывает в стейт пользователя необходимость загрузки фото, затем выдает клавиатуру выбора количетсва фото
    - Если выбран 'no', записывает в стейт пользователя отсутствие необходимости загрузки фото, соличетсво фото ставит 0, записывает заду запрса
    и перенаправляет в получение результата
    :param call:CallbackQuery
    """

    if call.data == 'yes':
        Users_State.state_record(user_id=call.from_user.id, key='photo', value=True)
        bot.edit_message_text(
            message_id=call.message.message_id, chat_id=call.message.chat.id,
            text=SELECT_COUNT_PHOTO[Users_State.state_get(user_id=call.from_user.id, key='lang')],
            reply_markup=hotels_count_keys(COUNT_PHOTO_CALL))

    else:
        Users_State.state_record(user_id=call.from_user.id,
                                 key=('photo', 'photo_count', 'date'),
                                 value=(False, 0, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')))
        get_result(call=call)


@bot.callback_query_handler(func=lambda call: call.data in COUNT_PHOTO_CALL.keys())
def callback_photo_count(call: CallbackQuery) -> None:
    """
    Шаг 7а:
    Хандоер инлайн-клавиатуры количества фотографий. Реагирует только на COUNT_PHOTO_CALL.keys()
    После выбора количества фото - записывает в стейт пользователя необходимость загрузки фото, их количество и дату создания запроса.
    Затем перенаправляет в функцию получения результата.
    :param call: CallbackQuery
    :return:
    """

    count_photo = COUNT_PHOTO_CALL[call.data]
    lang = Users_State.state_get(user_id=call.from_user.id, key='lang')

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=CHOICE_COUNT_PHOTO[lang].format(str(count_photo))
    )

    Users_State.state_record(user_id=call.from_user.id, key=('photo_count', 'date'),
                             value=(
                                 count_photo, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')))

    get_result(call=call)


def get_result(call: CallbackQuery):
    lang, command, city, curr, check_in, check_out, hotel_count, photo_count = \
        Users_State.state_get(user_id=call.from_user.id, key=('lang', 'command', 'city', 'curr', 'check_in', 'check_out', 'hotel_count', 'photo_count'))

    if command == LOWPRICE_CALL:
        cap = LOWPRICE_STAE[lang]
    else:
        cap = HIGHPRICE_STATE[lang]

    bot.send_message(chat_id=call.from_user.id,
                     text=request_card_builder(template=REQUEST_CARD_TEMPLATE[lang],
                                               param=(cap, city, curr, check_in, check_out, hotel_count, photo_count)) + '\n' + PLEASE_WHAIT[lang],
                     parse_mode='html')

    response = request_hotel_search(user_id=call.from_user.id)

    if response.status_code == 200:
        hotel_list = json.loads(response.text)['data']['body']['searchResults']['results']
        if hotel_list is False:
            bot.send_message(chat_id=call.from_user.id, text=NOT_FOUND[lang])
        elif command != BESTDEAL_CALL:
            show_result(user_id=call.from_user.id, hotel_list=hotel_list)
        else:
            print('заглушка')

    else:
        bot.send_message(chat_id=call.from_user.id, text=ERROR_HOTEL[lang])
        bot.delete_state(user_id=call.from_user.id)
        text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS[lang].items()]
        bot.send_message(chat_id=call.from_user.id, text='\n'.join(text), reply_markup=main_menu_keys(lang))


def get_media(hotel_id: int, text: str) -> list:
    count_photo = 3
    response_photo = request_get_photo(hotel_id=hotel_id)
    if response_photo.status_code == 200:
        photo_list = json.loads(response_photo.text)['hotelImages']
        media_massive = []
        for link_photo in photo_list:
            if count_photo == 0:
                return media_massive
            else:
                photo = link_photo['baseUrl'].format(size='w')
                response = requests.get(photo)
                if response.status_code == 200:
                    count_photo -= 1
                    media_massive.append(
                        InputMediaPhoto(photo, caption=text if count_photo == 1 else '', parse_mode='html')
                    )


def show_result(user_id: int, hotel_list: dict) -> None:
    lang, count_hotel, f_hotel = Users_State.state_get(user_id=user_id, key=('lang', 'hotel_count', 'photo'))
    for hotel in hotel_list:
        if count_hotel != 0:
            i_hotel = HOTEL_TEMPLATE[lang].format(
                hotel['name'],
                f'{hotel["address"]["streetAddress"]}, {hotel["address"]["locality"]}, {hotel["address"]["countryName"]}, {hotel["address"]["postalCode"]}',
                hotel['landmarks'][0]['distance'],
                hotel['ratePlan']['price']['current'],
                hotel['starRating'],
                URL_HOTEL.format(hotel['id'])
            )
            if not f_hotel:
                bot.send_message(chat_id=user_id, text=i_hotel, parse_mode='html')
            else:
                bot.send_media_group(chat_id=user_id, media=get_media_file(hotel['id'], user_id, i_hotel))
        else:
            bot.send_message(chat_id=user_id, text=SEARCH_COMPLETE)
            break
        count_hotel -= 1


def get_media_file(hotel_id: int, user_id: int, text: str) -> list:
    count_photo = Users_State.state_get(user_id=user_id, key='photo_count')
    response_photo = request_get_photo(hotel_id=hotel_id)
    if response_photo.status_code == 200:
        photo_list = json.loads(response_photo.text)['hotelImages']
        print(photo_list)
        media_massive = []
        for link_photo in photo_list:
            if count_photo == 0:
                return media_massive
            else:
                photo = link_photo['baseUrl'].format(size='w')
                response = requests.get(photo, timeout=15)
                if response.status_code == 200:
                    count_photo -= 1
                    media_massive.append(
                        InputMediaPhoto(photo, caption=text if count_photo == 1 else '', parse_mode='html')
                    )
