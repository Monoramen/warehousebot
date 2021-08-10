import re
#rack_list = WarehouseItem.objects.filter(Q(rack='C1'))
from rack_choices import RACK_CHOICES

racks = []
for index in RACK_CHOICES:
    stellazh = index[1][1]

    if index[1][1] in racks:
        pass
    else:
        racks.append(stellazh)

print(racks)

for index in racks:
    result = re.findall(f'С{index}-П\d-М\d', str(RACK_CHOICES))
    for i in range(0, len(result), 2):
        print(result[i])