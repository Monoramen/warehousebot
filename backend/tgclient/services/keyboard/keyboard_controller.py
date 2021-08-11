from typing import List, NamedTuple, Optional
from tgclient.models import WarehouseItem


class ItemInfo(NamedTuple):
    id: int
    product: str
    info: str
    quantity: int
    rack: str


class ItemFilter:
    def search_name(self, name):
        self.items = WarehouseItem.objects.filter(product__name__icontains=name)
        return self.items
    
    def search_rack(self, rack):
        self.items = WarehouseItem.objects.filter(rack__contains=rack)
        return self.items


#def _get_info(text_message:str) -> ItemInfo:
    