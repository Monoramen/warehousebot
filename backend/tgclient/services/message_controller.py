from .message_db import insert_user_id
from typing import List, NamedTuple, Optional





class ProfileInfo(NamedTuple):
    """Структура распаршенного сообщения объекта пользователя склада"""
    id: int
    username: str
    first_name: str
    last_name: str

def add_update_info(raw_message:str):
    data = _get_info(raw_message)
    return insert_user_id(data)

def _get_info(raw_message:str) -> ProfileInfo:
    chat_id = raw_message.chat_id
    username = raw_message.from_user.username
    first_name = raw_message.from_user.first_name
    last_name = raw_message.from_user.last_name

    return ProfileInfo(id=chat_id, username=username, first_name=first_name, last_name=last_name)



    