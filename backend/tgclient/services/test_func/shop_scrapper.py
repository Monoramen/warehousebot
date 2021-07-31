import datetime
from collections import namedtuple
from re import T, split
from typing import Pattern
from bs4 import BeautifulSoup
import requests
from requests.api import get


######
InnerBlock = namedtuple('Block', 'title, price, url')

class Block(InnerBlock):
    def __str__(self) -> str:
        return f'{self.title} \t {self.price} \t {self.url}'

######
class Parse_item_chipdip:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
            'Accept-Language': 'ru',
        }

    def get_page(self, search_field,  page: int = None):
        #параметры запроса
        params = {}
        if page and page > 1:
            params['page'] = page

        url = 'https://www.chipdip.ru/search?searchtext={}'.format(search_field)
        r = self.session.get(url=url, params=params)
        return r.text    

    @staticmethod
    def parse_data(search_field):
        item = Parse_item_chipdip().get_page(search_field)
        #return print(item)
        soup = BeautifulSoup(item, 'html.parser')
        div = soup.findAll('div')
        div = soup.find( 'table', {'class': 'itemlist'} )
        items = div.find_all_next( 'div', {'class': 'name'} )
        
        reply = ''
        for item in items:
            #reply += ' ' + item
            print(item.text)





page = Parse_item_chipdip()
results = page.parse_data('ST-151001')


print(results)
