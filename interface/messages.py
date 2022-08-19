from keyboards.key_text import *


DEFAULT_COMMANDS = {
    'Ru': {
        'start': "Запустить бота",
        'help': "Вывести справку",
        LOWPRICE_CALL: "Самые дешёвые отели в городе",
        HIGHPRICE_CALL: "Самые дорогие отели в городе",
        HISTORY_CALL: "История поиска отелей",
        SET_LANG_CALL: "Сменить язык интерфейса"
    },
    'En': {
        'start': "Bot start",
        'help': "Get the help",
        LOWPRICE_CALL: "The cheapest hotels in the city",
        HIGHPRICE_CALL: "The most expensive hotels in the city",
        HISTORY_CALL: "Hotel search history",
        SET_LANG_CALL: "Change the interface language"
    }
}

DEFAULT_COMMANDS_MENU = {
    'start': "Запустить бота / Bot start"
}

SELECT_LANG = 'Выберите язык интерфейа\n' \
              'Select interface laguage'

CHOICE_LANG = {
    'Ru': 'Выбран Русский язык',
    'En': 'English is selected'
}
