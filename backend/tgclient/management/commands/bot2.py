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
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, ParseMode, InputTextMessageContent)
from telegram.ext import (CallbackContext, Filters, 
    MessageHandler, Updater,
    CommandHandler, CallbackContext,
    Filters, ConversationHandler,
    InlineQueryHandler,
)
from telegram.update import Update
from telegram.utils.request import Request
from telegram.utils.helpers import escape_markdown
from tgclient.models import Message
from tgclient.models import Profile
from tgclient.models import WarehouseItem
from tgclient.services.message_controller import add_update_info
from tgclient.services.message_db import show_all_item
from django.db.models import Q

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
PRODUCT, QUANTITY, CONFIRMATION = range(3)
CHAT_TIMEOUT=60

def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message =f'Error!!!: {e}'
            print(error_message)
        return inner


def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(update: Update, _: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    query = query.strip().lower()
    logger.info('inine: %s', query)
    results = []
    query_list = WarehouseItem.objects.filter(Q(product__name__icontains=query))
    try:
        for i, (name) in enumerate(query_list):
            results.append(
                InlineQueryResultArticle(
                    id=i+1,
                    title=f'{name.product}',
                    description=f'количество {name.quantity} шт., место: {name.rack}, {name.receipt_date}',
                    input_message_content=InputTextMessageContent(
                        message_text= '{}'.format(name),
                    )
                )
            )
        if query and not results:
            results.append(
                InlineQueryResultArticle(
                    id=1000,
                    title='Не найдено',
                    input_message_content=InputTextMessageContent(
                        message_text= f'Ничего не найдено по запросу -> "{query}" ',
                    )
                )
            )     
        update.inline_query.answer(
            results=results,
            cache_time=20,
        )
    except AttributeError as ex:
        return   

def show_warehouse(update: Update, context: CallbackContext) -> str:    
    update.message.reply_text(text='', parse_mode='Markdown') 

class Command(BaseCommand):
    help = 'TgWarehouseBot'

    def handle(self, *args, **options):
        request = Request(
            con_pool_size=10,
            connect_timeout=0.5,
            read_timeout=1.0
        )     
        
        bot = Bot(request=request, token=settings.TOKEN)
        updater = Updater(bot=bot, use_context= True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(InlineQueryHandler(inlinequery))
        dp.add_handler(CommandHandler('showall' ,show_warehouse))
        dp.add_error_handler(error)
        
        updater.start_polling()
        updater.idle()