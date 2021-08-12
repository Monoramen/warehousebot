import re

data_list = ['Object '+str(i) for i in range(1, 21, 1)]

print(data_list)




def paginator(data:list, n:int):
    pages = [data[i:i+n] for i in range(0, len(data), n)]
    print('Pages = ', len(pages))
    return print(pages)

paginator(data_list, 10)