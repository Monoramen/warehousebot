from .message_db import insert_user_id
from typing import List, NamedTuple, Optional





class ProfileInfo(NamedTuple):
    """Структура распаршенного сообщения объекта пользователя склада"""
    external_id: int
    name: str

def add_update_info(raw_message:str):
    data = _get_info(raw_message)
    return '{}'.format(insert_user_id(data))

def _get_info(raw_message:str) -> ProfileInfo:
    chat_id = raw_message.chat_id
    name = raw_message.from_user.name
    return ProfileInfo(external_id=chat_id, name=name)



    