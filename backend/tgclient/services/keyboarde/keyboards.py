import builtins
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)
from tgclient.models import WarehouseItem
from django.db.models import Q
import re
from . import keyboard_db
from tgclient.rack_choices import RACK_CHOICES


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


def item_edit_info(name):
    items = WarehouseItem.objects.filter(product__name__icontains=name)
    print(items)
    btn_list  = []
    for index, (name) in enumerate(items):
        #result += f'количество {name.quantity} шт., место: {name.rack}, {name.product.info} '
        keyboard = [InlineKeyboardButton(text = f'кол-во {name.quantity}', callback_data = 'EDIT_Q'), InlineKeyboardButton(text = f'место {name.rack}', callback_data = name.rack)]
    btn_list.append(keyboard)
    btn_list.append(footer_kb)

    return InlineKeyboardMarkup(btn_list) 


class ButtonsInline:
    def __init__(self, data_list: list, width: int):
        self.data_list = data_list
        self.width = width
        self.button_list  = []
        self.keys_list = []
        self.row = []
        self.counter = 0

    def create_buttons(self):
        for item in self.data_list:
            key = InlineKeyboardButton(text = item, callback_data = item)
            self.keys_list.append(key)

        for item in self.keys_list:
            self.row.append(item)
            self.counter += 1
            if self.counter == self.width:
                self.button_list.append(self.row)
                self.row = []
                self.counter = 0
            if self.counter == 1 and item == self.keys_list[-1]:
                self.button_list.append(self.row)
            else:
                pass
        self.button_list.append(footer_kb)   
        return self.button_list


    def new(cls):
        params = cls.create_buttons()
        
        return InlineKeyboardMarkup(params)
