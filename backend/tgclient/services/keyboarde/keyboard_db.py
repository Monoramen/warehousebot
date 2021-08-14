from re import S
from typing import List, NamedTuple, Optional
from tgclient.models import WarehouseItem


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
        self.items = WarehouseItem.objects.filter(rack__contains=rack)
        for item in self.items:
            self.product_name.append(item.product.name)
        
        return self.product_name

    