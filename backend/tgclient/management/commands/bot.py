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
    logger.info('Command: %s', '/start was press')
    add_update_info(update.message)
    
    update.message.reply_text(MESSAGE['start'], parse_mode='Markdown')


def help_command(update: Update, context: CallbackContext) -> None:
    logger.info('Command: %s', '/help')
    """Send a message when the command /help is issued."""
    update.message.reply_text(MESSAGE['help'], parse_mode='Markdown')

def photo(update, context) -> None:
    file_id = update.message.photo[-1].file_id
    newFile=context.bot.get_file(file_id)
    url= newFile.file_path
    reply = detect_barcode(url)
    update.message.reply_text(' Штрихкод {}'.format(reply),  parse_mode='Markdown')


def inlinequery(update: Update, _: CallbackContext) -> None:
    """Handle the inline query."""
    picture = 'http://s1.iconbird.com/ico/0512/48pxwebiconset/w48h481337350005System.png'
    query = update.inline_query.query
    offset = int(update.inline_query.offset) if update.inline_query.offset else 0
    logger.info('inine: %s', query)
    results = []
    query_list = WarehouseItem.objects.filter(Q(product__name__icontains=query.strip().lower()))

   
    results = []
    try:
        for index, (name) in enumerate(query_list):
            try:
                results.append(
                    InlineQueryResultArticle(
                        id=str(offset + index),
                        title=f'{name.product}',
                        description=f'{name.product.info} количество {name.quantity} шт., место: {name.rack}, {name.receipt_date}',
                        input_message_content=InputTextMessageContent(
                            message_text= '{}'.format(name),
                        ),
                        thumb_url=picture, thumb_width=48, thumb_height=48
                    )
                )
            
            except Exception as e:
                print(e)

            except Exception as e:
                print(e)
    
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
        
        update.inline_query.answer(results=results, cache_time=20, auto_pagination=True)    
    
    except Exception as e:
        print(e)


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
        dp.add_handler(MessageHandler(Filters.photo & ~Filters.command, photo))
        dp.add_error_handler(error)
        
        updater.start_polling()
        updater.idle()