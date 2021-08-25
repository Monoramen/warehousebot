# -*- coding: UTF-8 -*-
from typing import List, NamedTuple, Optional

START = ''' *Привет, я заведую складом*  {}
'''
HELP = '''
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    1. /start - регистрация или обновление данных пользователя
    2. /help - помощь
    3. /menu - меню управления товаром (если хочешь посмотреть, что лежит на стеллаже, или хочешь изменить)
    4. /cancel - отмена 
    5. Напиши @WarehouseMTbot для того чтобы найти и поделиться

'''
BYE = '''
_Удачи. До скорого!_ {}
'''

EDIT_STEP = """
:page_facing_up: *Выбран:* {}
*Чтобы изменить количество:* _напиши число в формате от -100000 до 10000 *( - вычитание, + добавление)* из общего количества._ :black_nib:
*Чтобы изменить местоположение:*  _111м или 213м\n(1 - Стеллаж, 2 - Полка, 3 - Место)\n_:pushpin:
"""

MENU_MSG = """
        :black_large_square: *МЕНЮ* :black_large_square:\n
1. В стеллажах можно просматривать и изменять элементы.\n
2. Найти элемент (не доступно). Доступен поиск -> @WarehouseMTbot

"""


MESSAGE = {
    'start': START + HELP,
    'help': HELP,
    'bye': BYE, 
    'edit_step': EDIT_STEP,
    'menu_msg': MENU_MSG,

}
    
def data_item_pattern(data:NamedTuple) -> str:
    answer = f'*{data.product}*\n_{data.info}_\n*КОЛИЧЕСТВО:* {data.quantity} шт.\n*МЕСТО:* {data.rack}'
    return answer
    
