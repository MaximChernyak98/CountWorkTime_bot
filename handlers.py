import datetime

import settings
import config
import utils
import dialogues


def greeting(update, context):
    config.CHAT_ID = update.message.chat.id
    print(config.CHAT_ID)
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
    dialogues.print_message_with_keyboard(question_message, buttons_text_list)
    return 'wait_answer'


def print_rest_fallback(update, context):
    update.message.reply_text('Просто пришли цифру от 1 до 99, не выделывайся:)')


def end_of_day(update, context):
    update.callback_query.answer('Рабочий день закончен!')
    end_of_day_message = dialogues.send_end_of_day_message()
    update.callback_query.edit_message_text(text=end_of_day_message)


def current_result_of_day(update, context):
    if settings.SUMMARY_WORK_TIME > settings.HOURS_FOR_WORK_AT_DAY:
        can_user_go_home = 'Тебя никто не осудит, если ты пойдешь домой'
    else:
        can_user_go_home = 'Солнце еще высоко, клубника сама себя не вырастит!:)'
    current_result_message = f'''
Сегодня потрачено на работу - {utils.timedelta_to_time_string(settings.SUMMARY_WORK_TIME, full_format=True)};
Ты отдыхал - {utils.timedelta_to_time_string(settings.SUMMARY_BREAK_TIME, full_format=True)}
Обедал - {utils.timedelta_to_time_string(settings.SUMMARY_DINNER_TIME, full_format=True)}
{can_user_go_home}
'''
    update.message.reply_text(text=current_result_message)
