
import sqlite3
from pathlib import Path
from typing import NamedTuple
from sqlite3 import Error
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def sql_connection():
    try:
        con = sqlite3.connect('db.sqlite3')
        return con
    except Error:
        print(Error)

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM sqlite_master')
    con.commit()

con = sql_connection()
sql_table(con)

def edit_rack():
    con = sql_connection()
    sql_table(con)




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

