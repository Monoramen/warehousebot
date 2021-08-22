from os import name
from tgclient.models import ProfileTelegram



def insert_user_id(data: dict):
    if not ProfileTelegram.objects.filter(tg_id=data.id):
        try:
            p, _ = ProfileTelegram.objects.get_or_create(
                tg_id=data.id, 
                tg_username=data.username,
                tg_first_name = data.first_name,
                tg_last_name = data.last_name,

                defaults={'tg_username': data.username,}
                )
            return 'Регистрация прошла успешно'
        except:
            pass
    else:
        return
