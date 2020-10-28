import settings
import config
import utils


def greeting(update, context):
    config.CHAT_ID = update.message.chat.id
    message = '''Привет! Я бот, который поможет тебе подсчитать рабочее время \
и время отдыха. Включи камеру и я начну работу'''
    update.message.reply_text(message)


def end_of_day(update, context):
    update.callback_query.answer('Рабочий день закончен!')
    end_of_day_message = f'''
Поздравляю с окончанием рабочего дня!\nРезультат на сегодня:
Рабочее время - {utils.timedelta_to_time_string(settings.SUMMARY_WORK_TIME)};
Время перерывов - {utils.timedelta_to_time_string(settings.SUMMARY_BREAK_TIME)}
Время обеда - {utils.timedelta_to_time_string(settings.SUMMARY_DINNER_TIME)}
'''
    update.callback_query.edit_message_text(text=end_of_day_message)


def mini_break(update, context):
    update.callback_query.answer('Понял, жду возвращения')
    mini_break_message = 'Объявлен мини-перерыв, жду возвращения'
    update.callback_query.edit_message_text(text=mini_break_message)
