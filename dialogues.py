import config
import settings
import utils
import google_spreadsheet

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def form_main_keyboard():
    keyboard_buttons = [["Продолжить работу", "Завершить работу", "Результаты дня"]]
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
    # buttons_text_list ('button_text', 'button_callback_data')
    buttons_text_list = [('Рабочий день закончен', 'end_workday'),
                         ('Отошел, но еще вернусь', 'mini_break')]
    message = 'Пропал с радаров, рабочий день закончен или перерыв?'
    print_message_with_keyboard(message, buttons_text_list)


def send_return_to_workspace_message():
    # buttons_text_list ('button_text', 'button_callback_data')
    buttons_text_list = [('Отдых', 'rest'),
                         ('Рабочий вопрос', 'work'),
                         ('Обед', 'dinner')]
    message = 'Снова тебя вижу, по какому вопросу отходил?'
    print_message_with_keyboard(message, buttons_text_list)


def send_end_of_day_message(*args):
    end_of_day_message = f'''
Поздравляю с окончанием рабочего дня!\nРезультат на сегодня:
Рабочее время - {utils.timedelta_to_time_string(settings.SUMMARY_WORK_TIME, full_format=True)};
Время перерывов - {utils.timedelta_to_time_string(settings.SUMMARY_BREAK_TIME, full_format=True)}
Время обеда - {utils.timedelta_to_time_string(settings.SUMMARY_DINNER_TIME, full_format=True)}
'''
    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text=end_of_day_message)
    if settings.USE_GOOGLE_SPREADSHEET:
        date = datetime.datetime.today().strftime('%d.%m.%Y')
        work_time = utils.timedelta_to_time_string(settings.SUMMARY_WORK_TIME, full_format=False)
        break_time = utils.timedelta_to_time_string(settings.SUMMARY_BREAK_TIME, full_format=False)
        dinner_time = utils.timedelta_to_time_string(settings.SUMMARY_DINNER_TIME, full_format=False)
        new_row = [date, work_time, break_time, dinner_time]
        google_spreadsheet.GOOGLE_WORKSHEET.append_row(new_row)
    return end_of_day_message
