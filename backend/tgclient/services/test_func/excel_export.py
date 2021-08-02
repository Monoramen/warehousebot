from os import name
import pandas as pd
import os


pre = os.path.dirname(os.path.realpath(__file__))
print(pre)

file = 'prod_list.xlsx'
path = os.path.join(pre, file)
df = pd.read_excel(path, engine = 'openpyxl')

names, articles = df['Name'].tolist(), df['Article'].tolist()
prod_list = dict(zip(names, articles))


#for key, value in prod_list.items():
#    print(key,' ',value)

#print(prod_list)