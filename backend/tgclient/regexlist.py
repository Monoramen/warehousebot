import re
from rack_choices import RACK_CHOICES

quantity = r'^\d{,5}$'
rack = r'^\d{,3}м$'

#print(RACK_CHOICES)

for item in RACK_CHOICES:
    if 'С3-П3-М3' in item:
        print(item)

test = RACK_CHOICES.index(('С3-П3-М3', 'С3-П3-М3'))
#print(re.match('С3-П3-М3', RACK_CHOICES))
print(test)
def edit_handler(string:str):
    patterns = [r'^[-+]?\d{,5}$', r'^\d{,3}м$']
    
    for i in range(0, len(patterns), 1):
        result = re.match(patterns[i], string)
        if result and i == 0:
            return print(10 + int(result.group(0)))
        if result and i == 1:
            rack = 'С{}-П{}-М{}'.format(result.group(0)[0], result.group(0)[1], result.group(0)[2]) 
            return rack
        elif result == None:
            return
