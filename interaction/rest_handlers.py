import settings
import config
from interaction.dialogues import form_main_keyboard
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup
from helpers.timedelta_to_str import timedelta_to_time_string
from helpers.utils import prepare_part_time_for_print


def full_rest(update, context):
    type_rest = None
    if settings.REST_TIME_TYPE == 'rest':
        settings.SUMMARY_BREAK_TIME += settings.RAW_BREAK_TIME
        type_rest = 'в перерыв'
    elif settings.REST_TIME_TYPE == 'work':
        settings.SUMMARY_WORK_TIME += settings.RAW_BREAK_TIME
        type_rest = 'в рабочее время'
    else:
        settings.SUMMARY_DINNER_TIME += settings.RAW_BREAK_TIME
        type_rest = 'в обед'
    break_time_message = timedelta_to_time_string(settings.RAW_BREAK_TIME, full_format=True)
    update.callback_query.edit_message_text(text=f'Добавлено {break_time_message} {type_rest}')
    return ConversationHandler.END


def part_rest(update, context):
    settings.MYBOT.bot.delete_message(chat_id=config.CHAT_ID,
                                      message_id=update.callback_query.message.message_id)
    reply_keyboard = [["10", "30", "50", "70", "90"]]
    reply_text = None
    if settings.REST_TIME_TYPE == 'rest' or settings.REST_TIME_TYPE == 'dinner':
        reply_text = 'Введи процент рабочего времени'
    else:
        reply_text = 'Введи процент отдыха'

    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID,
                                    text=reply_text,
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                     resize_keyboard=True,
                                                                     one_time_keyboard=True))
    return 'get_percent'


def count_rest_part(update, context):
    percent = int(update.message.text)
    if 1 < percent < 100:
        first_time, first_message, second_time, second_message = prepare_part_time_for_print(percent)
        if settings.REST_TIME_TYPE == 'rest':
            settings.SUMMARY_WORK_TIME += first_time
            first_message += ' в рабочее время'
            settings.SUMMARY_BREAK_TIME += second_time
            second_message += ' в отдых'
        elif settings.REST_TIME_TYPE == 'work':
            settings.SUMMARY_WORK_TIME += first_time
            first_message += ' в отдых'
            settings.SUMMARY_BREAK_TIME += second_time
            second_message += ' в рабочее время'
        else:
            settings.SUMMARY_WORK_TIME += first_time
            first_message += ' в рабочее время'
            settings.SUMMARY_DINNER_TIME += second_time
            second_message += ' в обед'
        part_rest_message = f'Записал:\n{first_message}\n{second_message}'
        update.message.reply_text(text=part_rest_message, reply_markup=form_main_keyboard())
        return ConversationHandler.END
    else:
        update.message.reply_text(text=f'Введи, пожалуйста, число от 1 до 99')
        return 'get_percent'
