from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from tgclient.models import WarehouseItem

rack_list = WarehouseItem.objects.filter(Q(product__name__icontains=query.strip().lower()))

MENU = range(1)
SHOW, EDIT, DONE, BACK, SEARCH = range(5)

menu_kb =  InlineKeyboardMarkup([
        [InlineKeyboardButton("Показать стеллажи", callback_data=str(SHOW)), InlineKeyboardButton("Найти/Изменить", callback_data=str(SEARCH))], 
        [InlineKeyboardButton("Завершить", callback_data=str(DONE))],
    ])


rack_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("C1", callback_data='1')],
        [InlineKeyboardButton("Назад", callback_data=str(BACK))],
        ])