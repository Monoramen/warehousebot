from typing import Pattern
from bs4 import BeautifulSoup
import requests


import requests
from bs4 import BeautifulSoup

class Parse_item_chipdip():
    def get_data(self, article):
        result = requests.get('https://www.chipdip.ru/search?searchtext={}'.format(article))
        self.soup = BeautifulSoup(result.text, 'html.parser')
        div = self.soup.findAll('div')
        soup = self.soup
        div = soup.find( 'table', {'class': 'itemlist'} )
        tr = div.find( 'tr', {'class': 'with-hover'} )
        item = tr.find('a', {'class': 'link'})
       
        reply = item.text
        return reply

answer = Parse_weather()
weather = answer.get_data('C4532X5R0J107MT000N')

print(weather)
