import builtins
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)
from tgclient.models import WarehouseItem
from django.db.models import Q
import re
from . import keyboard_db
import emoji
MENU, RACK, ITEMS, ITEM, EDIT = range(5)
SHOW, DONE, BACK, SEARCH = range(4)
footer_kb =  [ InlineKeyboardButton("Назад", callback_data=str(BACK))]

done_kb = InlineKeyboardButton(emoji.emojize(':heavy_check_mark: Завершить', use_aliases=True), callback_data=str(DONE))


menu_kb =  InlineKeyboardMarkup([
        [InlineKeyboardButton('Cтеллажи', callback_data=str(SHOW)), InlineKeyboardButton('Найти', callback_data=str(SEARCH))],
        [done_kb],
    ])

edit_kb = InlineKeyboardMarkup([
    [InlineKeyboardButton('Назад', callback_data=str(BACK)), done_kb ]
    ])




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