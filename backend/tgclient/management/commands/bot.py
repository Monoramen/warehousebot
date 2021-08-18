from os import kill, name, replace
import logging
from uuid import uuid4
from logging import error
from cv2 import data
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram import (InlineQueryResultArticle, ParseMode, InputTextMessageContent)
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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from django.db.models import Q
from tgclient.services.keyboard_inline import paginator as pg
from tgclient.models import WarehouseItem
from tgclient.services.keyboard_inline import keyboards as kb
from tgclient.services.message.message_controller import add_update_info
from tgclient.services.barcode.detect_barcode import detect_barcode
from .messages import MESSAGE

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

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
                        description=f'количество {name.quantity} шт., место: {name.rack}, {name.receipt_date} {name.product.info} ',
                        input_message_content=InputTextMessageContent(
                            message_text= f'{name}  {name.product.info}',
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

MENU, RACK, ITEM = range(3)
SHOW, EDIT, DONE, BACK, SEARCH, ITEMS = range(6)
data_list = [] 

def menu(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    update.message.reply_text('Выбери действие', reply_markup=kb.menu_kb)
    return MENU


def menu_over(update, _):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Выбери действие", reply_markup=kb.menu_kb)
    return MENU


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    print(query.data)


def rack_menu(update, _):
    query = update.callback_query
    query.answer()
    data = ['С'+str(i) for i in range(1,10, 1)]
    keyboard = kb.ButtonsInline(data, 3).new()
    query.edit_message_text(text=f"_", reply_markup=keyboard)
    return RACK
 

def place(update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    global inline_buttons_pages
    data_list = kb.keyboard_db.ItemFilter().new_rack_list(query.data)
    inline_buttons_pages = data_list
    print(inline_buttons_pages)
    query.answer()
    paginator = pg.InlineKeyboardPaginator(
        len(inline_buttons_pages),
        item_data=data_list,
        data_pattern='character#{page}'
    )

    query.edit_message_text(
        text=inline_buttons_pages[0],
        reply_markup=paginator.markup,
    )
    return ITEM



def place_page_callback(update, context):
    query = update.callback_query

    query.answer()

    page = int(query.data.split('#')[1])

    paginator = pg.InlineKeyboardPaginator(
        len(inline_buttons_pages),
        current_page=page,
        item_data=data_list,
        data_pattern='character#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Go back', callback_data=str(BACK)))

    query.edit_message_text(
        text=inline_buttons_pages[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
    return ITEM




def edit_step(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    data = kb.keyboard_db.ItemFilter().search_name(query.data)
    print(data)
    query.edit_message_text(text=f"Выбран: {query.data}", reply_markup=kb.item_edit_info(query.data))
    return ITEM


def done(update, _):
    """Возвращает `ConversationHandler.END`, который говорит 
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Увидимся еще')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Увидимся', reply_markup=kb.ReplyKeyboardRemove())
    return ConversationHandler.END


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


        menu_handler = ConversationHandler(
            entry_points=[CommandHandler("menu", menu)],
            states={# словарь состояний разговора, возвращаемых callback  функциями
                
                MENU: [
                    CallbackQueryHandler(menu_over, pattern='^' + str(BACK) + '$'),
                    CallbackQueryHandler(rack_menu, pattern='^' + str(SHOW) + '$'),
                    CallbackQueryHandler(done, pattern='^' + str(DONE) + '$'),    
                ],

                RACK: [
                    CallbackQueryHandler(menu_over, pattern='^' + str(BACK) + '$'),
                    CallbackQueryHandler(done, pattern='^' + str(DONE) + '$'), 
                    CallbackQueryHandler(place,),  
                    
                ],

                ITEM: [
                    CallbackQueryHandler(menu_over, pattern='^' + str(BACK) + '$'),
                    CallbackQueryHandler(place_page_callback, pattern='^character#' ),
                    #CallbackQueryHandler(rack_menu, pattern='^' + str(BACK) + '$'),
                    #CallbackQueryHandler(edit_step), 
                    #CallbackQueryHandler(done, pattern='^' + str(DONE) + '$'),
                ],
                },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
            
        dp.add_handler(menu_handler)
        dp.add_handler(InlineQueryHandler(inlinequery))
        dp.add_handler(MessageHandler(Filters.photo & ~Filters.command, photo))
        dp.add_error_handler(error)
        
        updater.start_polling()
        updater.idle()