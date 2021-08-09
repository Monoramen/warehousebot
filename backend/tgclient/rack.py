import re
#rack_list = WarehouseItem.objects.filter(Q(rack='C1'))
from rack_choices import RACK_CHOICES
result = re.findall(r'С\d-П\d-М\d', str(RACK_CHOICES))
#print(result)
rack = str(RACK_CHOICES)

print(len(RACK_CHOICES))
print(RACK_CHOICES)
racks = []
for index in RACK_CHOICES:
    stellazh = index[1][1]

    if index[1][1] in racks:
        pass
    else:
        racks.append(stellazh)

print(racks)