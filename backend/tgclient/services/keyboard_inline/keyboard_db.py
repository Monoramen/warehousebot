from re import S
from typing import List, NamedTuple, Optional
from tgclient.models import WarehouseItem
import pickle
from django.db.models import Q, query
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

def update_quantity(items:list, digit:int):
    print('itemid', items.id)
    print('QUANTITY=', items.quantity)
    return WarehouseItem.objects.filter(id=items.id).update(quantity = digit)

def update_rack(items:list, rack:str):
    return WarehouseItem.objects.filter(id=items.id).update(rack = rack)

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