import settings
import config
import utils
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def full_rest(update, context):
    type_rest = None
    if settings.REST_TIME_TYPE == 'rest':
        settings.SUMMARY_BREAK_TIME += settings.RAW_BREAK_TIME
        update.callback_query.answer('Посчитал все в перерыв')
        type_rest = 'в перерыв'
    elif settings.REST_TIME_TYPE == 'work':
        settings.SUMMARY_WORK_TIME += settings.RAW_BREAK_TIME
        update.callback_query.answer('Посчитал все в рабочее')
        type_rest = 'в рабочее время'
    else:
        settings.SUMMARY_DINNER_TIME += settings.RAW_BREAK_TIME
        update.callback_query.answer('Посчитал все в обед')
        type_rest = 'в обед'
    break_time_message = utils.timedelta_to_time_string(settings.RAW_BREAK_TIME)
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
    first_part_time = None
    second_part_time = None
    first_part_message = None
    second_part_message = None
    if 1 < percent < 100:
        if settings.REST_TIME_TYPE == 'rest':
            first_part_time = settings.RAW_BREAK_TIME * percent / 100
            settings.SUMMARY_WORK_TIME += first_part_time
            first_part_message = utils.timedelta_to_time_string(first_part_time) + 'в рабочее время'
            second_part_time = settings.RAW_BREAK_TIME * (100 - percent) / 100
            settings.SUMMARY_BREAK_TIME += second_part_time
            second_part_message = utils.timedelta_to_time_string(second_part_time) + 'в отдых'
        elif settings.REST_TIME_TYPE == 'work':
            first_part_time = settings.RAW_BREAK_TIME * percent / 100
            settings.SUMMARY_WORK_TIME += first_part_time
            first_part_message = utils.timedelta_to_time_string(first_part_time) + 'в отдых'
            second_part_time = settings.RAW_BREAK_TIME * (100 - percent) / 100
            settings.SUMMARY_BREAK_TIME += second_part_time
            second_part_message = utils.timedelta_to_time_string(second_part_time) + 'в рабочее время'
        else:
            first_part_time = settings.RAW_BREAK_TIME * percent / 100
            settings.SUMMARY_WORK_TIME += first_part_time
            first_part_message = utils.timedelta_to_time_string(first_part_time) + 'в рабочее время'
            second_part_time = settings.RAW_BREAK_TIME * (100 - percent) / 100
            settings.SUMMARY_BREAK_TIME += second_part_time
            second_part_message = utils.timedelta_to_time_string(second_part_time) + 'в обед'
        part_rest_message = f'Записал:\n{first_part_time} % в {first_part_message}' \
                            f'\n{second_part_time} % в {second_part_message}'
        update.message.reply_text(text=part_rest_message,
                                  reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        update.message.reply_text(text=f'Введи, пожалуйста, число от 1 до 99')
        return 'get_percent'
