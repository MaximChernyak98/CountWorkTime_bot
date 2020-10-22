import settings
import config
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup


def full_rest(update, context):
    if settings.REST_TIME_TYPE == 'rest':
        settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text='Посчитал все в перерыв')
    elif settings.REST_TIME_TYPE == 'work':
        settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text='Посчитал все в рабочее время')
    else:
        settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text='Посчитал все в обед')
    return ConversationHandler.END


def part_rest(update, context):
    reply_keyboard = [["10", "30", "50", "70", "90"]]
    reply_text = ''

    if settings.REST_TIME_TYPE == 'rest' or settings.REST_TIME_TYPE == 'dinner':
        reply_text = 'Введи процент рабочего времени'
    else:
        reply_text = 'Введи процент отдыха'

    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID,
                                    text=reply_text,
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return 'get_percent'


def count_rest_part(update, context):
    if 1 < int(update.message.text) < 100:
        a = update.message.text
        if settings.REST_TIME_TYPE == 'rest' or settings.REST_TIME_TYPE == 'dinner':
            update.message.reply_text(text=f'Записал {a} % в рабочее время')
        else:
            update.message.reply_text(text=f'Записал {a} % в отдых')
        return ConversationHandler.END
    else:
        update.message.reply_text(text=f'Введи, пожалуйста, число от 1 до 99')
        return 'get_percent'
