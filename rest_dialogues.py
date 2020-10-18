import settings
import config
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup


def full_rest(update, context):
    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text='Посчитал все в перерыв')
    return ConversationHandler.END


def part_rest(update, context):
    reply_keyboard = [["10", "30", "50", "70", "90"]]
    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID,
                                    text='Введи процент рабочего времени',
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return 'get_percent'


def count_rest_part(update, context):
    if 1 < int(update.message.text) < 100:
        a = update.message.text
        update.message.reply_text(text=f'Получил число {a}')
        return ConversationHandler.END
    else:
        update.message.reply_text(text=f'Введи, пожалуйста, число от 1 до 99')
        return 'get_percent'
