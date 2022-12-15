"""
Сценарий команд lowprice, highprice.
"""

import datetime
import json
from typing import Any

from telebot.types import Message, CallbackQuery, InputMediaPhoto

from loader import bot
from config_data.API_requests import request_city_search, request_hotel_list, request_get_information
from database.structure import Data_request_state, DataBase, Users_State

from config_data.config import URL_HOTEL

from interface.messages import LOWPRICE_STAE, HIGHPRICE_STATE, SELECT_CITY, \
    INCORRECT_CITY, CORRECT_CITY, ERROR_CITY, CHOICE_CITY, \
    SELECT_COUNT_HOTEL, CHOICE_COUNT_HOTEL, SELECT_CHECK_IN, INCORRECT_CHECK_IN_FORMAT, INCORRECT_CHECK_IN_DATA, \
    SELECT_CHECK_OUT, INCORRECT_CHECK_OUT_FORMAT, INCORRECT_CHECK_OUT_DATA, SELECT_LOAD_PHOTO, SELECT_COUNT_PHOTO, \
    CHOICE_COUNT_PHOTO, PLEASE_WHAIT, ERROR_HOTEL, DEFAULT_COMMANDS, HOTEL_TEMPLATE, NOT_FOUND, SEARCH_COMPLETE, \
    REQUEST_CARD_TEMPLATE, SELECT_LOW_PRICE, BESTDEAL_STATE, REQUEST_CARD_TEMPLATE_BEST

from keyboards.key_text import LOWPRICE_CALL, COUNT_HOTEL_CALL, COUNT_PHOTO_CALL, BESTDEAL_CALL, \
    HIGHPRICE_CALL
from keyboards.keyboards import city_corr_keys, hotels_count_keys, select_photo_keys, main_menu_keys

from handlers.bestdeal import best_deal_select


def request_card_builder(user_id: int) -> tuple[str, str, str]:
    """
    Вспомогательная функция формирования итоговой карточки запроса

    :param user_id: id пользователя в телеграме,
    :return: tuple - Возвращает заполненную итоговую карточку запроса, команду и язык интерфейса
    """
    command, lang = Users_State.state_get(user_id=user_id, key=('command', 'lang'))

    if command == LOWPRICE_CALL:
        cap = LOWPRICE_STAE[lang]
    elif command == HIGHPRICE_CALL:
        cap = HIGHPRICE_STATE[lang]
    else:
        cap = BESTDEAL_STATE[lang]

    if command != BESTDEAL_CALL:
        user_info = Users_State.state_get(user_id=user_id, key=(
            'city', 'check_in', 'check_out', 'hotel_count', 'photo_count'))

        request_card = REQUEST_CARD_TEMPLATE[lang].format(cap, *user_info)

    else:
        user_info = Users_State.state_get(user_id=user_id, key=(
            'city', 'low_price', 'high_price', 'low_dist', 'high_dist', 'check_in', 'check_out',
            'hotel_count', 'photo_count'))

        request_card = REQUEST_CARD_TEMPLATE_BEST[lang].format(cap, *user_info)
    return request_card, command, lang


def abort_command(user_id: int, lang: str) -> None:
    bot.delete_state(user_id=user_id)
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS[lang].items()]
    bot.send_message(chat_id=user_id, text='\n'.join(text), reply_markup=main_menu_keys(lang))


def lowprice_higthprice_start(user_id: int, command: str) -> None:
    """
    Шаг 0:
    Начало сценария команд lowprice, hothprice.
    Сначала получает язык пользователя из БД.
    Затем устанавливает стейт выбора города
    В конце записывает в стейт пользователя параметры 'lang' и 'command' (язык и выбранная команда соответственно)

    :param user_id: int - id пользователя в телеграме,
    :param command: - выбранная команда
    """

    lang = DataBase.user_get_lang(user_id=user_id)

    bot.delete_state(user_id=user_id)
    bot.set_state(user_id=user_id, state=Data_request_state.city)

    Users_State.state_record(user_id=user_id, key=('lang', 'command'),
                             value=(lang, command))

    bot.send_message(chat_id=user_id, text=SELECT_CITY[lang])


@bot.message_handler(state=[Data_request_state.city, Data_request_state.check_in, Data_request_state.check_out],
                     commands=['start', 'help'])
def cancel(message: Message) -> None:
    """
    Хэндлер-функция прерывания сценария по команде /start, /help
    :param message: Message
    """
    abort_command(user_id=message.from_user.id,
                  lang=Users_State.state_get(user_id=message.from_user.id, key='lang'))


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

    if response.status_code != 200:
        bot.send_message(chat_id=message.from_user.id, text=ERROR_CITY[lang])
    else:
        data = json.loads(response.text)['sr']
        if data is False:
            bot.send_message(chat_id=message.from_user.id, text=INCORRECT_CITY[lang])
        else:
            city_name_list: list[str] = []
            city_id_list: list[str] = []
            for elem in data:
                try:
                    if elem['type'] == 'CITY':
                        city_name_list.append(
                            f'{elem["regionNames"]["lastSearchName"]}, {elem["hierarchyInfo"]["country"]["name"]}')
                        city_id_list.append(elem['gaiaId'])
                except KeyError:
                    pass

            city_list = list(zip(city_name_list, city_id_list))
            if city_list is False:
                bot.send_message(chat_id=message.from_user.id, text=INCORRECT_CITY[lang])
            else:
                bot.send_message(chat_id=message.from_user.id, text=CORRECT_CITY[lang],
                                 reply_markup=city_corr_keys(city_list))


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def callback_city(call: CallbackQuery) -> None:
    """
    Шаг 2:
    Хэндлер-обработчик инлайн-клавиатуры уточнения города.
    После выбора какого-либо города записывает название города и его id в стейт пользователя.
    После чего выдает клавиатуру выбора валюты.
    :param call: CallbackQuery
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
             chat_id=call.from_user.id, text=SELECT_COUNT_HOTEL[lang],
             reply_markup=hotels_count_keys(COUNT_HOTEL_CALL))

    # bot.send_message(
    #     chat_id=call.from_user.id, text=SELECT_CURRENCY[lang],
    #     reply_markup=currency_keys()
    # )


# @bot.callback_query_handler(func=lambda call: call.data in CURRENCY_KEY_CALL)
# def callback_currency(call: CallbackQuery) -> None:
#     """
#     Шаг 3:
#     Хэндлер-обработчик инлайн-клавиатуры выбора валюты. Реагирует только на CURRENCY_KEY_CALL
#     После выбора валюты записывает её в стейт пользователя.
#     В конце выдает клавиатуру выбора количества отображаемых отелей.
#     :param call: CallbackQuery
#     """
#
#     lang = Users_State.state_get(user_id=call.from_user.id, key='lang')
#     bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
#     bot.edit_message_text(
#         chat_id=call.message.chat.id, message_id=call.message.message_id,
#         text=CHOICE_CURRENCY[lang].format(call.data)
#     )
#
#     Users_State.state_record(user_id=call.from_user.id, key='curr', value=call.data)
#     bot.send_message(
#         chat_id=call.from_user.id, text=SELECT_COUNT_HOTEL[lang],
#         reply_markup=hotels_count_keys(COUNT_HOTEL_CALL)
#     )


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
    lang, command = Users_State.state_get(user_id=call.from_user.id, key=('lang', 'command'))

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=CHOICE_COUNT_HOTEL[lang].format(str(count_hotel))
    )

    Users_State.state_record(user_id=call.from_user.id, key='hotel_count', value=count_hotel)

    if command != BESTDEAL_CALL:
        bot.set_state(user_id=call.from_user.id, state=Data_request_state.check_in)
        bot.send_message(
            chat_id=call.from_user.id, text=SELECT_CHECK_IN[lang]
        )
    else:
        bot.set_state(user_id=call.from_user.id, state=Data_request_state.low_price)
        bot.send_message(
            chat_id=call.from_user.id, text=SELECT_LOW_PRICE[lang])



@bot.message_handler(state=Data_request_state.check_in)
def check_in_handler(message: Message) -> None:
    """
    Шаг 5:
    Хэндлер стейта check_in. Осуществляет проверку ввода пользователя по двум параметрам:
    - Формат даты
    - Дата не должна быть раньше текущей.
    Если все в порядке - записывает данные в стейт пользователя и устанавливает стейт check_out
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
    Если все в порядке - записывает данные в стейт пользователя и выдает клавиатуру на выбор необходимости загрузки фото отеля
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
    и перенаправляет в получение результата.
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
        get_result_hotel(call=call)


@bot.callback_query_handler(func=lambda call: call.data in COUNT_PHOTO_CALL.keys())
def callback_photo_count(call: CallbackQuery) -> None:
    """
    Шаг 7а:
    Хандоер инлайн-клавиатуры количества фотографий. Реагирует только на COUNT_PHOTO_CALL.keys()
    После выбора количества фото - записывает в стейт пользователя необходимость загрузки фото, их количество и дату создания запроса.
    Затем перенаправляет в функцию получения результата.
    :param call: CallbackQuery
    """

    count_photo = COUNT_PHOTO_CALL[call.data]
    lang, command = Users_State.state_get(user_id=call.from_user.id, key=('lang', 'command'))

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=CHOICE_COUNT_PHOTO[lang].format(str(count_photo))
    )

    Users_State.state_record(user_id=call.from_user.id, key=('photo_count', 'date'),
                             value=(
                                 count_photo, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')))

    get_result_hotel(call=call)


def get_result_hotel(call: CallbackQuery):
    Users_State.state_print(user_id=call.from_user.id)
    request_card, command, lang = request_card_builder(user_id=call.from_user.id)

    bot.send_message(chat_id=call.from_user.id,
                     text=request_card + '\n' + PLEASE_WHAIT[lang], parse_mode='html')
    response = request_hotel_list(user_id=call.from_user.id, command=command)

    if response.status_code == 200:
        try:
            hotel_list_draft: list[dict] = json.loads(response.text)['data']['propertySearch']['properties']
        except (KeyError, TypeError):
            bot.send_message(chat_id=call.from_user.id, text=NOT_FOUND[lang])
            abort_command(user_id=call.from_user.id, lang=lang)
        else:
            hotel_list: list[dict] = []
            hotel_count = Users_State.state_get(user_id=call.from_user.id, key='hotel_count')
            for elem in hotel_list_draft:
                if hotel_count == 0:
                    break
                else:
                    hotel_list.append(elem)
                    hotel_count -= 1

            show_result(user_id=call.from_user.id, hotel_list=hotel_list, request_card=request_card)

    else:
        bot.send_message(chat_id=call.from_user.id, text=ERROR_HOTEL[lang])
        abort_command(user_id=call.from_user.id, lang=lang)


def show_result(user_id: int, hotel_list: list[dict], request_card: str) -> None:
    lang, f_hotel, command = Users_State.state_get(user_id=user_id, key=('lang', 'photo', 'command'))
    if command == BESTDEAL_CALL:
        hotel_list = best_deal_select(hotel_list=hotel_list, user_id=user_id)

    DataBase.request_set(user_id=user_id, content=request_card)
    for hotel in hotel_list:
        try:
            hotel_id = hotel["id"]
            if not f_hotel:

                i_hotel = HOTEL_TEMPLATE[lang].format(
                    hotel["name"],
                    f'{get_hotel_info(hotel_id=hotel_id, user_id=user_id)}',
                    hotel["destinationInfo"]["distanceFromDestination"]["value"],
                    hotel["mapMarker"]["label"],
                    hotel["reviews"]["score"],
                    URL_HOTEL.format(hotel['id']))

                bot.send_message(chat_id=user_id, text=i_hotel, parse_mode='html')
            else:
                hotel_address, photo_list = get_hotel_info_photo(hotel_id=hotel_id, user_id=user_id)
                media_massive = []

                i_hotel = HOTEL_TEMPLATE[lang].format(
                    hotel["name"],
                    f'{hotel_address}',
                    hotel["destinationInfo"]["distanceFromDestination"]["value"],
                    hotel["mapMarker"]["label"],
                    hotel["reviews"]["score"],
                    URL_HOTEL.format(hotel['id']))

                DataBase.hotels_set(user_id=user_id, content=i_hotel, photo='\n'.join(photo_list))
                for photo in photo_list:
                    media_massive.append(InputMediaPhoto(photo, caption=i_hotel if photo == photo_list[-1] else '', parse_mode='html'))
                bot.send_media_group(chat_id=user_id, media=media_massive)


        except KeyError:
            pass

    else:
        bot.send_message(chat_id=user_id, text=SEARCH_COMPLETE[lang])
        abort_command(user_id=user_id, lang=lang)


def get_hotel_info(hotel_id: int, user_id: int) -> str:
    response = request_get_information(user_id=user_id, hotel_id=hotel_id)
    hotel_address = ''
    if response.status_code == 200:
        hotel_info = json.loads(response.text)
        try:
            hotel_address = hotel_info["data"]["propertyInfo"]["summary"]["location"]["address"][
                "addressLine"]
        except KeyError:
            pass
    return hotel_address


def get_hotel_info_photo(hotel_id: int, user_id: int) -> tuple[Any, list[Any]]:
    response = request_get_information(user_id=user_id, hotel_id=hotel_id)
    photo_list = []
    hotel_address = ''
    if response.status_code == 200:
        hotel_info = json.loads(response.text)
        try:
            hotel_address = hotel_info["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"]
            hotel_photo_count = Users_State.state_get(user_id=user_id, key='photo_count')
            hotel_info_photo = hotel_info["data"]["propertyInfo"]["propertyGallery"]["images"]
            for photo_url in hotel_info_photo:
                if hotel_photo_count != 0:
                    photo_list.append(photo_url["image"]["url"])
                    hotel_photo_count -= 1
                else:
                    break

        except KeyError:
            pass
    return hotel_address, photo_list
