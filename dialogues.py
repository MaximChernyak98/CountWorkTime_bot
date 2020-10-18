import config
import settings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def print_message_with_keyboard(message, buttons_text_list):
    keyboard = []
    for button in buttons_text_list:
        keyboard.append(InlineKeyboardButton(button[0], callback_data=button[1]))
    reply_markup = InlineKeyboardMarkup([keyboard])
    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text=message, reply_markup=reply_markup)


def print_first_message():
    first_message = f'Вижу тебя, с началом рабочего дня!'
    settings.MYBOT.bot.send_message(chat_id=config.CHAT_ID, text=first_message)


def send_left_from_workspace_message():
    # buttons_text_list ('button_text', 'button_callback_data')
    buttons_text_list = [('Рабочий день закончен', 'end_workday'),
                         ('Отошел, но еще вернусь', 'mini_break')]
    message = 'Снова тебя вижу, по какому вопросу отходил?'
    print_message_with_keyboard(message, buttons_text_list)


def send_return_to_workspace_message():
    # buttons_text_list ('button_text', 'button_callback_data')
    buttons_text_list = [('Отдых', 'rest'),
                         ('Рабочий вопрос', 'work_issue'),
                         ('Обед', 'dinner')]
    message = 'Снова тебя вижу, по какому вопросу отходил?'
    print_message_with_keyboard(message, buttons_text_list)


def rest_message(update, context):
    # buttons_text_list ('button_text', 'button_callback_data')
    buttons_text_list = [('Все время отдыхал', 'full_rest'),
                         ('Еще и поработал', 'partial_rest')]
    message = 'Все ли время отдыхал или удалось порешать рабочие вопросики?'
    print_message_with_keyboard(message, buttons_text_list)
    return 'wait_answer'
