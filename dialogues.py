import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def return_to_workspace_message(context):
    keyboard = [[InlineKeyboardButton("Отдых", callback_data='rest'),
                 InlineKeyboardButton("Рабочий вопрос", callback_data='work_issue'),
                 InlineKeyboardButton("Обед", callback_data='dinner')
                 ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return_message = 'Снова тебя вижу, по какому вопросу отходил?'
    context.bot.send_message(chat_id=config.CHAT_ID, text=return_message, reply_markup=reply_markup)


def left_from_workspace_message(context):
    keyboard = [[InlineKeyboardButton("Рабочий день закончен", callback_data='end_workday'),
                 InlineKeyboardButton("Отошел, но еще вернусь", callback_data='mini_break')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    left_message = 'Ты пропал с радаров, рабочий день закончен или еще вернешься?'
    context.bot.send_message(chat_id=config.CHAT_ID, text=left_message, reply_markup=reply_markup)


def print_first_message(mybot):
    first_message = f'Вижу тебя, с началом рабочего дня!'
    mybot.bot.send_message(chat_id=config.CHAT_ID, text=first_message)


def print_return_to_workspace_dialogue(mybot):
    mybot.job_queue.run_once(callback=return_to_workspace_message, when=1)


def print_left_workspace_dialogue(mybot):
    mybot.job_queue.run_once(callback=left_from_workspace_message, when=1)
