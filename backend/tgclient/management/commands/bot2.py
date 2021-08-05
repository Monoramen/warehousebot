from os import name
import re
import logging
from uuid import uuid4
from logging import error
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import query_utils
from telegram import Bot
from telegram import Update
from telegram import PhotoSize
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, ParseMode, InputTextMessageContent)
from telegram.ext import (CallbackContext, Filters, 
    MessageHandler, Updater,
    CommandHandler, CallbackContext,
    Filters, ConversationHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
)
from telegram.update import Update
from telegram.utils.request import Request
from telegram.utils.helpers import escape_markdown
from tgclient.models import WarehouseItem

from django.db.models import Q
from .messages import MESSAGE
from django.conf import settings
from tgclient.services.message.message_controller import add_update_info
from tgclient.services.barcode.detect_barcode import detect_barcode

def inlinequery(update: Update, _: CallbackContext) -> None:
    query = update.inline_query.query
    query = query.strip().lower()
    logger.info('inine: %s', query)
    picture = divide_icon
    query_list = WarehouseItem.objects.filter(Q(product__name__icontains=query))
    offset = int(query.offset) if query.offset else 0
    results = []
    if len(query_list) is 0:
        try:
            result = InlineQueryResultArticle(
                    id=1000,
                    title='Не найдено',
                    input_message_content=InputTextMessageContent(
                        message_text= f'Ничего не найдено по запросу -> "{query}" ',
                    )
                )
            
            update.inline_query.answer(query.id, [result], cache_time=20,)
        except Exception as e:
            print(e)
        return
    results_array = []
    try:
        m_next_offset = str(offset + 5) if len(query_list) == 5 else None
        for i, (name) in enumerate(query_list):
            try:
                # При использовании подгрузки, ID должны быть уникальными в пределах всей большой пачки!
                results_array.append(InlineQueryResultArticle(id=str(offset + i),
                    title=f'{name.product}',
                    description=f'количество {name.quantity} шт., место: {name.rack}, {name.receipt_date}',
                    input_message_content=InputTextMessageContent(
                        message_text= '{}'.format(name),
                        ),
                        thumb_url=picture, thumb_width=48, thumb_height=48)
                    )

            except Exception as e:
                print(e)
        # устанавливаем новый offset или сбрасываем, если в БД закончились релевантные записи
        update.answer_inline_query.answer(query.id, results_array, next_offset=m_next_offset if m_next_offset else "")
    except Exception as e:
        print(e)
def inlinequery(update: Update, _: CallbackContext) -> None:
    """Handle the inline query."""
    picture = divide_icon
    query = update.inline_query.query
    offset = int(query.offset) if query.offset else 0
    logger.info('inine: %s', query)
    results = []
    query_list = WarehouseItem.objects.filter(Q(product__name__icontains=query.strip().lower()))

    if len(query_list) is 0:
        try:
            result = InlineQueryResultArticle(
                    id=1000,
                    title='Не найдено',
                )
            update.inline_query.answer(query.id, [result])
        except Exception as e:
            print(e)
        return    
    results = []
    try:
        m_next_offset = str(offset + 5) if len(query_list) == 5 else None
        for i, (name) in enumerate(query_list):
            results.append(
                InlineQueryResultArticle(
                    id=str(),
                    title=f'{name.product}',
                    description=f'количество {name.quantity} шт., место: {name.rack}, {name.receipt_date}',
                    input_message_content=InputTextMessageContent(
                        message_text= '{}'.format(name),
                    ),
                    thumb_url=picture, thumb_width=48, thumb_height=48
                )
            )
        if query and not results:
            results.append(
                
            )
        
        print(len(results))
        update.inline_query.answer(
            results=results,
            cache_time=20,
        )
    except Exception as e:
        print(e)
    except AttributeError as ex:
        return 
