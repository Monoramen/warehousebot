import re

quantity = r'^\d{,5}$'
rack = r'^\d{,3}м$'

def edit_handler(string:str):
    patterns = [r'^\d{,5}$', '^\d{,3}м$']
    try:
        for pattern in patterns:
            result = re.match(pattern, string)
            if result:
                return print(result.group(0))
    except Exception as e:
        print(e)



filter(input('введите '))