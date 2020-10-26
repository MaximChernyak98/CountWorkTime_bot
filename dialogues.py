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
                         ('Рабочий вопрос', 'work'),
                         ('Обед', 'dinner')]
    message = 'Снова тебя вижу, по какому вопросу отходил?'
    print_message_with_keyboard(message, buttons_text_list)


def rest_message(update, context):
    pushed_button = ''
    buttons_text_list = []
    message = ''
    pushed_button = update.callback_query.data

    # buttons_text_list ('button_text', 'button_callback_data')
    if pushed_button == 'rest':
        buttons_text_list = [('Все время отдыхал', 'full_rest'),
                             ('Еще и поработал', 'partial_rest')]
        message = 'Все ли время отдыхал или удалось порешать рабочие вопросики?'
        settings.REST_TIME_TYPE = 'rest'
    elif pushed_button == 'work':
        buttons_text_list = [('Все время работал', 'full_rest'),
                             ('Еще и вафлил', 'partial_rest')]
        message = 'Все ли время посвятил рабочему вопросу?'
        settings.REST_TIME_TYPE = 'work'
    else:
        buttons_text_list = [('Все время ел', 'full_rest'),
                             ('Еще и поработал', 'partial_rest')]
        message = 'Все ли время посвятил обеду или обкашливал рабочие вопросы?'
        settings.REST_TIME_TYPE = 'dinner'
    print_message_with_keyboard(message, buttons_text_list)
    return 'wait_answer'
