import builtins
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from tgclient.models import WarehouseItem
from django.db.models import Q
import re
#rack_list = WarehouseItem.objects.filter(Q(rack='C1'))
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
    rack_keys.append('C' + i)    



MENU  = range(1)
SHOW, EDIT, DONE, BACK, SEARCH = range(5)
footer_kb =  [InlineKeyboardButton("Завершить", callback_data=str(DONE)), InlineKeyboardButton("Назад", callback_data=str(BACK))]

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


     

