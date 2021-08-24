import logging
from logging import error
from threading import TIMEOUT_MAX
from emoji import emojize as emg
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q, query
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup,
                    InlineQueryResultArticle, InputTextMessageContent,
                    ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                        CommandHandler, ConversationHandler, Filters,
                        InlineQueryHandler, MessageHandler, Updater)
from telegram.update import Update
from telegram.utils.helpers import escape_markdown
from telegram.utils.request import Request
from tgclient.models import WarehouseItem
from tgclient.services.barcode.detect_barcode import detect_barcode
from tgclient.services.keyboard_inline import keyboards as kb
from tgclient.services.keyboard_inline import paginator as pg
from tgclient.services.message.message_controller import add_update_info
from .messages import MESSAGE, data_item_pattern

"""" MENU """
MENU, RACK, ITEMS, ITEM, EDIT = range(5)
SHOW, DONE, BACK, SEARCH = range(4)
CHAT_TIMEOUT=2

global item_data_edit ####Turple with data selected item

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

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
    update.message.reply_text(MESSAGE['start'].format(emg(':new_moon_with_face:',  use_aliases=True)),  parse_mode='Markdown')

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

def menu(update: Update, context: CallbackContext) -> None:
    logger.info('Inline MENU start: %s', update.message.from_user.username )
    """Sends a message with three inline buttons attached."""
    update.message.reply_text(text=emg(MESSAGE['menu_msg'], use_aliases=True), reply_markup=kb.menu_kb,parse_mode='Markdown')
    return MENU

def menu_over(update, _):
    query = update.callback_query
    query.answer()
    logger.info('Inline MENU return: %s', query.data)
    query.edit_message_text(text=f"======*Выбери действие*======", reply_markup=kb.menu_kb,parse_mode='Markdown')
    return MENU

def rack_menu(update, _):
    query = update.callback_query
    query.answer()
    logger.info('Inline RACK menu return: %s', query.data)
    data = ['С'+str(i) for i in range(1, 10, 1)]
    keyboard = kb.ButtonsInline(data, 3).new()
    query.edit_message_text(text=f"----------*Стеллажи*----------", reply_markup=keyboard,  parse_mode='Markdown')
    return RACK

def place(update, _):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    logger.info('Inline RACK place return: %s', query.data)
    global inline_buttons_pages
    inline_buttons_pages = kb.keyboard_db.ItemFilter().search_rack(query.data)
    query.answer()
    paginator = pg.InlineKeyboardPaginator(
        len(inline_buttons_pages),
        item_data=inline_buttons_pages,
        data_pattern='items#{page}'
    )
    paginator.add_before(InlineKeyboardButton('Добавить', callback_data='add'))
    paginator.add_after(InlineKeyboardButton(emg(':arrow_left: Назад', use_aliases=True), callback_data=str(SHOW)))
    query.edit_message_text(
        text=f'*{query.data} Страница 1 *',
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
    return ITEMS

def place_page_callback(update, _):
    query = update.callback_query
    query.answer()
    page = int(query.data.split('#')[1])
    logger.info('Inline RACK place callback return: %s', query.data)
    global inline_buttons_pages
    paginator = pg.InlineKeyboardPaginator(
        len(inline_buttons_pages),
        current_page=page,
        item_data=inline_buttons_pages,
        data_pattern='items#{page}'
    )
    paginator.add_before(InlineKeyboardButton('Добавить', callback_data='add'))
    paginator.add_after(InlineKeyboardButton('Назад', callback_data=str(SHOW)))
    query.edit_message_text(
        text=f'* Страница {page}*',
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
    return ITEMS

def edit_step(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    global item_data_edit ####Turple with data selected item
    item_data_edit = kb.keyboard_db.ItemFilter().search_name(query.data)
    logger.info('Inline EDIT step callback return: %s', item_data_edit)
    if item_data_edit == None:
        return ITEMS
    else:
        query.edit_message_text(
            text=emg(MESSAGE['edit_step'].format(data_item_pattern(item_data_edit)),  use_aliases=True),
            reply_markup=kb.edit_kb,
            parse_mode='Markdown')
        return EDIT

def get_count(update: Update, context: CallbackContext):
    string = update.message.text
    global item_data_edit
    update.message.reply_text(
        text=f"*{item_data_edit.product}*\n {kb.keyboard_db.ItemEdit(item_data_edit, string).edit_handler()} \n",
        parse_mode='Markdown')
    return EDIT

def done(update, _):
    """Возвращает `ConversationHandler.END`, который говорит 
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()

    logger.info('Inline DONE return: %s', query.data)
    query.edit_message_text(MESSAGE['bye'].format(emg(':eyes:', use_aliases=True)),  parse_mode='Markdown')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.username)
    update.message.reply_text(MESSAGE['bye'].format(emg(':panda_face:',  use_aliases=True)), parse_mode='Markdown')
    return ConversationHandler.END

def timeout(update, context):
    update.message.reply_text('out time has ended. good bye')

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
            states={
                MENU: [
                    CallbackQueryHandler(rack_menu, pattern='^' + str(SHOW) + '$'),
                    CallbackQueryHandler(done, pattern='^' + str(DONE) + '$'),
                    CallbackQueryHandler(menu_over, pattern='^' + str(BACK) + '$'), 
                ],
                RACK: [
                    CallbackQueryHandler(menu_over, pattern='^' + str(BACK) + '$'),
                    CallbackQueryHandler(place, pattern='^..'),  
                    CallbackQueryHandler(done, pattern='^' + str(DONE) + '$'), 
                ],
                ITEMS: [
                    CallbackQueryHandler(rack_menu, pattern='^' + str(SHOW) + '$'),
                    CallbackQueryHandler(place_page_callback, pattern='^items#' ),
                    CallbackQueryHandler(edit_step, pattern='^....'),
                ],
                ITEM: [
                    CallbackQueryHandler(place,  str(BACK) ),
                    CallbackQueryHandler(edit_step, pattern='^....'),
                    
                ],
                EDIT: [
                    CallbackQueryHandler(rack_menu,  pattern='^' + str(BACK) + '$'),
                    CallbackQueryHandler(done, pattern='^' + str(DONE) + '$'), 
                    MessageHandler(Filters.regex(r'^[-+]?\S+$'), get_count),
                ],
                ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)],
                },
            fallbacks=[CommandHandler("cancel", cancel)],
            conversation_timeout=TIMEOUT_MAX,
            )
        dp.add_handler(menu_handler)
        dp.add_handler(InlineQueryHandler(inlinequery))
        dp.add_handler(MessageHandler(Filters.photo & ~Filters.command, photo))
        dp.add_error_handler(error)
        updater.start_polling()
        updater.idle()