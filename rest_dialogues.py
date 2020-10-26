import settings
import config
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup


def full_rest(update, context):
    if settings.REST_TIME_TYPE == 'rest':
        settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text='Посчитал все в перерыв')
        settings.SUMMARY_BREAK_TIME += settings.RAW_BREAK_TIME
    elif settings.REST_TIME_TYPE == 'work':
        settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text='Посчитал все в рабочее время')
        settings.SUMMARY_WORK_TIME += settings.RAW_BREAK_TIME
    else:
        settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text='Посчитал все в обед')
        settings.SUMMARY_DINNER_TIME += settings.RAW_BREAK_TIME
    return ConversationHandler.END


def part_rest(update, context):
    reply_keyboard = [["10", "30", "50", "70", "90"]]
    reply_text = None
    
    if settings.REST_TIME_TYPE == 'rest' or settings.REST_TIME_TYPE == 'dinner':
        reply_text = 'Введи процент рабочего времени'
    else:
        reply_text = 'Введи процент отдыха'

    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID,
                                    text=reply_text,
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return 'get_percent'


def count_rest_part(update, context):
    percent = int(update.message.text)
    if 1 < percent < 100:
        if settings.REST_TIME_TYPE == 'rest':
            settings.SUMMARY_WORK_TIME += settings.RAW_BREAK_TIME * percent / 100
            settings.SUMMARY_BREAK_TIME += settings.RAW_BREAK_TIME * (100 - percent) / 100
            update.message.reply_text(text=f'Записал {percent} % в рабочее время')
        elif settings.REST_TIME_TYPE == 'work':
            settings.SUMMARY_WORK_TIME += settings.RAW_BREAK_TIME * percent / 100
            settings.SUMMARY_BREAK_TIME += settings.RAW_BREAK_TIME * (100 - percent) / 100
            update.message.reply_text(text=f'Записал {percent} % в отдых')
        else:
            settings.SUMMARY_WORK_TIME += settings.RAW_BREAK_TIME * percent / 100
            settings.SUMMARY_DINNER_TIME += settings.RAW_BREAK_TIME * (100 - percent) / 100
            update.message.reply_text(text=f'Записал {percent} % в рабочее время')
        return ConversationHandler.END
    else:
        update.message.reply_text(text=f'Введи, пожалуйста, число от 1 до 99')
        return 'get_percent'
