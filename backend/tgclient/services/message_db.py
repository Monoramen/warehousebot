from os import name
from tgclient.models import Profile, Message, Product, WarehouseItem



def insert_user_id(data: dict):
    print(f'{data.external_id} {data.name}')
    if not Profile.objects.filter(external_id=data.external_id):
        try:
            p, _ = Profile.objects.get_or_create(external_id=data.external_id, 
            name=data.name,
            defaults={'name': data.name,}
            )
            return 'Регистрация прошла успешно'
        except:
            pass
    else:
        return

       
def show_all_item():
    items  = WarehouseItem.objects.all()
    list_item = f'Всего элементов {len(items)}: \n'
    for i in items:
        list_item += '`'+ str(i.product.name)+ '`' + ' *' +str(i.rack) + '*\n'
    
    return list_item