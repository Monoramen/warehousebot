from re import S
from typing import List, NamedTuple, Optional
from tgclient.models import WarehouseItem
import pickle

class ItemInfo(NamedTuple):
    id: int
    product: str
    info: str
    quantity: int
    rack: str

def _get_info(items:list) -> ItemInfo:
    for item in items:
        id = item.product.id
        product = item.product.name
        info = item.product.info
        quantity = item.quantity
        rack = item.rack

    return ItemInfo(
        id=item.product.id,
        product=item.product.name,
        info=item.product.info,
        quantity=item.quantity,
        rack=item.rack)

class ItemFilter:
    def __init__(self) -> None:
        self.product_info = list()
        

    def search_name(self, name):
        qs = WarehouseItem.objects.filter(product__name__icontains=name)
        reloaded_qs = WarehouseItem.objects.all()
        reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
        self.items = reloaded_qs 
        print('Полученные данные', self.items)
        for item in self.items:
            print(item.product.name)
            print(item.product.info)
            print(item.rack)
            print(item.status)
            print(item.quantity)
            info = f'*{item.product.name}* \n_{item.product.info}_\nНаходится -> *{item.rack}*\nКол-во: {item.quantity} шт.'
        data = _get_info(self.items)
        print(data)
        return  info
        
    def search_rack(self, rack):
        qs = WarehouseItem.objects.filter(rack__contains=rack)
        reloaded_qs = WarehouseItem.objects.all()
        reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
        self.items = reloaded_qs 
        if self.items:
            for item in self.items:
                self.product_info.append(item.product.name)
            items_group = [ self.product_info[i:i+5] for i in range(0, len(self.product_info), 5)]
        else:
            items_group = ['пусто']

        return items_group

    def new_rack_list(cls, name):
        params = cls.search_rack(name)
        return params
    