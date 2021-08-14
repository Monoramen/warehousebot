import builtins
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)
from tgclient.models import WarehouseItem
from django.db.models import Q
import re
from . import keyboard_db

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
            key = InlineKeyboardButton(text = item[:50], callback_data = item[:50])
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

    def buttons(cls):
        params = cls.create_buttons()
        return params


class PaginationInlineButtons:
    def __init__(self, button_list):
        n = 5
        self.button_list = button_list
        self.page_list = [self.button_list[i:i+n] for i in range(0, len(self.button_list), n)]

    def pagination(self):
        print(len(self.page_list))
        if len(self.page_list) == 1:
            page = InlineKeyboardMarkup(self.page_list[0])
        else:
            for i in len(self.page_list):
                page = InlineKeyboardMarkup(self.page_list[i])
            pass
        return page
