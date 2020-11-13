import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

import config
import settings
from helpers.timedelta_to_str import timedelta_to_time_string
from helpers.google_spreadsheet import GOOGLE_WORKSHEET


def form_main_keyboard():
    keyboard_buttons = [['Завершить работу', 'Результаты дня'], ['Поставить Pomodoro', 'Текущая Pomodoro']]
    main_keyboard = ReplyKeyboardMarkup(keyboard_buttons, resize_keyboard=True)
    return main_keyboard


def print_first_message():
    first_message = f'Вижу тебя, с началом рабочего дня!'
    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text=first_message, reply_markup=form_main_keyboard())


def print_message_with_keyboard(message, buttons_text_list):
    keyboard = []
    for button in buttons_text_list:
        keyboard.append(InlineKeyboardButton(button[0], callback_data=button[1]))
    reply_markup = InlineKeyboardMarkup([keyboard])
    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text=message, reply_markup=reply_markup)


def send_left_from_workspace_message():
    message = 'Пропал с радаров, рабочий день закончен или перерыв?'
    # buttons_text_list ('button_text', 'button_callback_data')
    buttons_text_list = [('Рабочий день закончен', 'end_workday'),
                         ('Отошел, но еще вернусь', 'mini_break')]
    print_message_with_keyboard(message, buttons_text_list)


def send_return_to_workspace_message():
    message = 'Снова тебя вижу, по какому вопросу отходил?'
    # buttons_text_list ('button_text', 'button_callback_data')
    buttons_text_list = [('Отдых', 'rest'),
                         ('Рабочий вопрос', 'work'),
                         ('Обед', 'dinner')]
    print_message_with_keyboard(message, buttons_text_list)


def send_end_of_day_message():
    end_of_day_message = f'''
Поздравляю с окончанием рабочего дня!\nРезультат на сегодня:
Рабочее время - {timedelta_to_time_string(settings.SUMMARY_WORK_TIME, full_format=True)};
Время перерывов - {timedelta_to_time_string(settings.SUMMARY_BREAK_TIME, full_format=True)}
Время обеда - {timedelta_to_time_string(settings.SUMMARY_DINNER_TIME, full_format=True)}
'''
    if settings.USE_GOOGLE_SPREADSHEET:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        date = datetime.datetime.today().strftime('%d.%m.%Y')
        work_time = timedelta_to_time_string(settings.SUMMARY_WORK_TIME, full_format=False)
        break_time = timedelta_to_time_string(settings.SUMMARY_BREAK_TIME, full_format=False)
        dinner_time = timedelta_to_time_string(settings.SUMMARY_DINNER_TIME, full_format=False)
        new_row = [time, date, work_time, break_time, dinner_time]
        GOOGLE_WORKSHEET.append_row(new_row)
    return end_of_day_message


def send_pomodoro_message(update, context):
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
    pomodoro_message = settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text=reply_text)
    delete_message = context.job.context.get('delete_message')
    if delete_message:
        message_number = pomodoro_message.message_id
        settings.JQ.run_once(callback=delete_pomodoro_message, when=7, context={'deleting_message': message_number})
