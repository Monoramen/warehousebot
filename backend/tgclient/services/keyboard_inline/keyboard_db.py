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


class ItemFilter:
    def __init__(self) -> None:
        self.product_name = []
        
    def search_name(self, name):
        self.items = WarehouseItem.objects.filter(product__name__icontains=name)
        print(self.items)
        
    def search_rack(self, rack):
        qs = WarehouseItem.objects.filter(rack__contains=rack)
        reloaded_qs = WarehouseItem.objects.all()
        reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
        self.items = reloaded_qs 
        
        for item in self.items:
            self.product_name.append(item.product.name)
        items_group = [ self.product_name[i:i+5] for i in range(0, len(self.product_name), 5)]
        return items_group

    def new_rack_list(cls, name):
        params = cls.search_rack(name)
        return params
    