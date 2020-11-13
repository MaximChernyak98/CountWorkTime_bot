import datetime

import settings
import config
from helpers.utils import timedelta_to_time_string
from interaction.dialogues import (print_message_with_keyboard, send_end_of_day_message,
                                   form_main_keyboard, send_pomodoro_notification)
from telegram.ext import ConversationHandler


def greeting(update, context):
    config.CHAT_ID = update.message.chat.id
    message = '''Привет! Я бот, который поможет тебе подсчитать рабочее время \
и время отдыха. Включи камеру и я начну работу'''
    update.message.reply_text(message)


def cheat_code(update, context):
    settings.SUMMARY_WORK_TIME = settings.HOURS_FOR_WORK_AT_DAY + datetime.timedelta(minutes=1)


def mini_break(update, context):
    update.callback_query.answer('Понял, жду возвращения')
    mini_break_message = 'Объявлен мини-перерыв, жду возвращения'
    update.callback_query.edit_message_text(text=mini_break_message)


def rest_message(update, context):
    buttons_text_list = []
    question_message = None
    pushed_button = update.callback_query.data
    settings.MYBOT.bot.delete_message(chat_id=config.CHAT_ID,
                                      message_id=update.callback_query.message.message_id)

    # buttons_text_list ('button_text', 'button_callback_data')
    if pushed_button == 'rest':
        buttons_text_list = [('Все время отдыхал', 'full_rest'),
                             ('Еще и поработал', 'partial_rest')]
        question_message = 'Все ли время отдыхал или удалось порешать рабочие вопросики?'
        settings.REST_TIME_TYPE = 'rest'
    elif pushed_button == 'work':
        buttons_text_list = [('Все время работал', 'full_rest'),
                             ('Еще и вафлил', 'partial_rest')]
        question_message = 'Все ли время посвятил рабочему вопросу?'
        settings.REST_TIME_TYPE = 'work'
    else:
        buttons_text_list = [('Все время ел', 'full_rest'),
                             ('Еще и поработал', 'partial_rest')]
        question_message = 'Все ли время посвятил обеду или обкашливал рабочие вопросы?'
        settings.REST_TIME_TYPE = 'dinner'
    print_message_with_keyboard(question_message, buttons_text_list)
    return 'wait_answer'


def print_rest_fallback(update, context):
    update.message.reply_text('Просто пришли цифру от 1 до 99, не выделывайся:)')


def print_pomodoro_fallback(update, context):
    update.message.reply_text('Просто пришли цифру от 5 до 40, не выделывайся:)')


def end_of_day(update, context):
    end_of_day_message = send_end_of_day_message()
    if update.callback_query == None:
        settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text=end_of_day_message)
    else:
        update.callback_query.edit_message_text(text=end_of_day_message)
    settings.SUMMARY_WORK_TIME = datetime.timedelta()
    settings.SUMMARY_BREAK_TIME = datetime.timedelta()
    settings.SUMMARY_DINNER_TIME = datetime.timedelta()
    settings.RAW_BREAK_TIME = datetime.timedelta()
    settings.IS_MAN_AT_WORKPLACE = False
    settings.IS_WORKDAY_STARTED = False


def current_result_of_day(update, context):
    if settings.SUMMARY_WORK_TIME > settings.HOURS_FOR_WORK_AT_DAY:
        can_user_go_home = 'Тебя никто не осудит, если ты пойдешь домой'
    else:
        can_user_go_home = 'Солнце еще высоко, клубника сама себя не вырастит!:)'
    current_result_message = f'''
Сегодня:
Потрачено на работу - {timedelta_to_time_string(settings.SUMMARY_WORK_TIME, full_format=True)}
Ты отдыхал - {timedelta_to_time_string(settings.SUMMARY_BREAK_TIME, full_format=True)}
Обедал - {timedelta_to_time_string(settings.SUMMARY_DINNER_TIME, full_format=True)}
{can_user_go_home}
'''
    update.message.reply_text(text=current_result_message)


def set_pomadoro_timer(update, context):
    pomodoro_time = int(update.message.text)
    if 5 <= pomodoro_time <= 40:
        settings.JQ.run_once(callback=send_pomodoro_notification, when=5, context={'delete_message': True})
        settings.JQ.run_once(callback=send_pomodoro_notification, when=6, context={'delete_message': True})
        settings.JQ.run_once(callback=send_pomodoro_notification, when=7, context={'delete_message': False})
        set_pomoro_text = f'Поставил таймер на {pomodoro_time} минут'
        update.message.reply_text(text=set_pomoro_text, reply_markup=form_main_keyboard())
        return ConversationHandler.END
    else:
        update.message.reply_text(text=f'Введи, пожалуйста, от 5 до 40 минут')
        return 'get_pomadoro_time'
