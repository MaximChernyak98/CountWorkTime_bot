import datetime
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from interaction.dialogues import (form_main_keyboard, print_message_with_keyboard)

import config
import settings


def send_pomodoro_message(update, context):
    jobs_names = settings.JQ.get_jobs_by_name('send_pomodoro_notification')
    if jobs_names:
        end_time = jobs_names[0].next_t
        now_time = datetime.datetime.now(datetime.timezone.utc)
        end_of_next_pomodoro = end_time - now_time
        seconds = end_of_next_pomodoro.seconds
        minutes_for_print = (seconds % 3600) // 60
        seconds_for_print = seconds % 60
        message = (f'Уже есть активная Pomadoro до окончания осталось '
                   f'{minutes_for_print} минут и {seconds_for_print} секунд.')
        buttons_text_list = [('Удалить активную и запустить новую?', 'set_new_pomadoro')]
        print_message_with_keyboard(message, buttons_text_list)
        return ConversationHandler.END
    else:
        reply_text = 'Укажи время Pomodoro (от 5 до 40 минут)'
        reply_keyboard = [['5', '10', '15', '20', '25', '30', '35', '40']]
        settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID,
                                        text=reply_text,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                         resize_keyboard=True,
                                                                         one_time_keyboard=True
                                                                         )
                                        )
        return 'get_pomadoro_time'


def delete_pomodoro_message(context):
    deleting_message = context.job.context.get('deleting_message')
    settings.MYBOT.bot.delete_message(chat_id=config.CHAT_ID, message_id=deleting_message)


def send_pomodoro_notification(context):
    reply_text = 'Pomodoro кончилась'
    pomodoro_message = settings.MYBOT.bot.send_message(
        chat_id=config.CHAT_ID, text=reply_text)
    delete_message = context.job.context.get('delete_message')
    if delete_message:
        message_number = pomodoro_message.message_id
        settings.JQ.run_once(callback=delete_pomodoro_message, when=3, context={'deleting_message': message_number})


def set_pomadoro_timer(update, context):
    pomodoro_time = int(update.message.text)
    if 5 <= pomodoro_time <= 40:
        pomodoro_time_in_seconds = pomodoro_time * 60
        settings.JQ.run_once(callback=send_pomodoro_notification, when=pomodoro_time_in_seconds, context={
            'delete_message': True})
        settings.JQ.run_once(callback=send_pomodoro_notification, when=pomodoro_time_in_seconds + 1, context={
            'delete_message': True})
        settings.JQ.run_once(callback=send_pomodoro_notification, when=pomodoro_time_in_seconds + 2, context={
            'delete_message': False})
        set_pomoro_text = f'Поставил таймер на {pomodoro_time} минут'
        update.message.reply_text(
            text=set_pomoro_text, reply_markup=form_main_keyboard())
        return ConversationHandler.END
    else:
        update.message.reply_text(text=f'Введи, пожалуйста, от 5 до 40 минут')
        return 'get_pomadoro_time'


def delete_all_pomodoro(update, context):
    jobs_tuple = settings.JQ.get_jobs_by_name('send_pomodoro_notification')
    if jobs_tuple:
        for job in jobs_tuple:
            job.schedule_removal()
        update.callback_query.edit_message_text(
            text=f'Активная Pomodoro удалена')
        reply_text = 'Укажи время Pomodoro (от 5 до 40 минут)'
        reply_keyboard = [['5', '10', '15', '20', '25', '30', '35', '40']]
        settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID,
                                        text=reply_text,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                         resize_keyboard=True,
                                                                         one_time_keyboard=True
                                                                         )
                                        )
    return 'get_pomadoro_time'
