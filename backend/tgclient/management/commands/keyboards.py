import builtins
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)
from tgclient.models import WarehouseItem
from django.db.models import Q
import re

from tgclient.rack_choices import RACK_CHOICES

#print(len(RACK_CHOICES))
#print(RACK_CHOICES)
racks = []
rack_keys = []
for index in RACK_CHOICES:
    stellazh = index[1][1]
    if index[1][1] in racks:
        pass
    else:
        racks.append(stellazh)
for i in racks:
    rack_keys.append('С' + i)    



MENU, RACK = range(2)
SHOW, EDIT, DONE, BACK, SEARCH, ITEMS = range(6)
footer_kb =  [ InlineKeyboardButton("Назад", callback_data=str(BACK))]

menu_kb =  InlineKeyboardMarkup([
        [InlineKeyboardButton("Cтеллажи", callback_data=str(SHOW)), InlineKeyboardButton("Найти", callback_data=str(SEARCH))], 
        [InlineKeyboardButton("Завершить", callback_data=str(DONE))],
    ])


btn_list = []
for i in range(0,len(rack_keys),3):
    keyboard = [InlineKeyboardButton(text = rack_keys[i], callback_data= rack_keys[i]), 
        InlineKeyboardButton(text = rack_keys[i+1], callback_data=rack_keys[i+1]), 
         InlineKeyboardButton(text = rack_keys[i+2], callback_data=rack_keys[i+2]),
        ]
    btn_list.append(keyboard)
btn_list.append(footer_kb)
rack_kb = InlineKeyboardMarkup(btn_list)   



def items_list(rack):
    print(type(rack))
    print(rack)
    items_list = WarehouseItem.objects.filter(rack__contains=rack)
    btn_list  = []
    for item in items_list:
        keyboard = [InlineKeyboardButton(text = item.product.name, callback_data= item.product.name)]
        btn_list.append(keyboard)
    btn_list.append(footer_kb)
    return InlineKeyboardMarkup(btn_list)   


def item_edit_info(name):
    items = WarehouseItem.objects.filter(product__name__icontains=name)
    print(items)
    btn_list  = []
    for index, (name) in enumerate(items):
        #result += f'количество {name.quantity} шт., место: {name.rack}, {name.product.info} '
        keyboard = [InlineKeyboardButton(text = f'кол-во {name.quantity}', callback_data = name.quantity), InlineKeyboardButton(text = f'место {name.rack}', callback_data = name.rack)]
    btn_list.append(keyboard)
    btn_list.append(footer_kb)

    return InlineKeyboardMarkup(btn_list) 

