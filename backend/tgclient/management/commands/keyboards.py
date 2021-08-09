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
    rack_keys.append('Cтеллаж №' + i)    
print(type(rack_keys))

MENU  = range(1)
SHOW, EDIT, DONE, BACK, SEARCH = range(5)

menu_kb =  InlineKeyboardMarkup([
        [InlineKeyboardButton("Показать стеллажи", callback_data=str(SHOW)), InlineKeyboardButton("Найти/Изменить", callback_data=str(SEARCH))], 
        [InlineKeyboardButton("Завершить", callback_data=str(DONE))],
    ])


#rack_kb = InlineKeyboardMarkup([
#        [InlineKeyboardButton("C1", callback_data='1')],
#        [InlineKeyboardButton("Назад", callback_data=str(BACK))],
#        ])

print(type(rack_keys))
print(rack_keys)
print(type(len(rack_keys)))
btn_list = []

for i in range(0,len(rack_keys),3):
    print(str(i))
    keyboard = [InlineKeyboardButton(text = rack_keys[i], callback_data=str(i)), 
        InlineKeyboardButton(text = rack_keys[i+1], callback_data=rack_keys[i+1]), 
         InlineKeyboardButton(text = rack_keys[i+2], callback_data=rack_keys[i+2]),
        ]
    btn_list.append(keyboard)
btn_list.append( [InlineKeyboardButton("Завершить", callback_data=str(DONE)), InlineKeyboardButton("Назад", callback_data=str(BACK))])
rack_kb = InlineKeyboardMarkup(btn_list)   


     

