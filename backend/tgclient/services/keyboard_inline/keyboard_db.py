import pickle
import re
from typing import NamedTuple
from django.db.models import Q
from tgclient.models import WarehouseItem
from tgclient.rack_choices import RACK_CHOICES

class ItemInfo(NamedTuple):
    id: int
    product: str
    info: str
    quantity: int
    rack: str

def _get_info(items:list) -> ItemInfo:
    for item in items:
        id = int(item.id)
        product = item.product.name
        info = item.product.info
        quantity = item.quantity
        rack = item.rack
    return ItemInfo(id=id, product=product, info=info, quantity=quantity, rack=rack)


class ItemEdit:
    def __init__(self,  items: list, string:str) -> None:
        self.string = string
        self.items = items
        self.digit = int
        self.quantity = int
        self.rack = str
        self.product =  ItemFilter().search_name(self.items.product)
    def edit_handler(self):
        patterns = [r'^[-+]?\d{,5}$', r'^\d{,3}м$']
        for i in range(0, len(patterns), 1):
            result = re.match(patterns[i], self.string)
            if result and i == 0:
                self.digit = int(result.group(0))
                return self._update_quantity
            if result and i == 1:
                self.rack = 'С{}-П{}-М{}'.format(result.group(0)[0], result.group(0)[1], result.group(0)[2]) 
                return self._update_rack
            elif result == None:
                return

    @property
    def _update_quantity(self):
        if self.items.quantity + self.digit < 0:
            return 'Ты хочешь больше чем есть'
        else:
            self.quantity = self.product.quantity + self.digit
            WarehouseItem.objects.filter(id=self.items.id).update(quantity = self.quantity)
            return f'Теперь {self.quantity} штук'
    @property
    def _update_rack(self):
        choice = RACK_CHOICES.index((self.rack, self.rack))
        print(choice)
        if choice:
            WarehouseItem.objects.filter(id=self.items.id).update(rack = WarehouseItem.RACK_CHOICES.self.rack)
            return f'Теперь товар лежит тут > {self.rack}'
        else:
            return f'Такого места нет'


class ItemFilter:
    def __init__(self) -> None:
        self.product_info = list()
        
    def search_name(self, name):
        qs = WarehouseItem.objects.filter(product__name__icontains=name)
        reloaded_qs = WarehouseItem.objects.all()
        reloaded_qs.query = pickle.loads(pickle.dumps(qs.query)) 
        if qs:
            return   _get_info(reloaded_qs)
        else:
            pass

    def search_rack(self, rack):
        qs = WarehouseItem.objects.filter(rack__contains=rack)
        reloaded_qs = WarehouseItem.objects.all()
        reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))

        if reloaded_qs:
            for item in reloaded_qs:
                self.product_info.append(item.product.name)
            items_group = [ self.product_info[i:i+5] for i in range(0, len(self.product_info), 5)]
        else:
            items_group = [['пусто']]
        return items_group
    @property
    def search_set(name):
        qs =  WarehouseItem.objects.filter(Q(product__name__icontains=name))
        reloaded_qs = WarehouseItem.objects.all()
        reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
        return qs
