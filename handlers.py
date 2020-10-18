import settings


def end_of_day(update, context):
    update.callback_query.answer('Рабочий день закончен!')
    end_of_day_message = f'''
Поздравляю с окончанием рабочего дня!\nРезультат на сегодня:
Рабочее время - {settings.SUMMARY_WORK_TIME};
Время перерывов - {settings.SUMMARY_BREAK_TIME}
'''
    update.callback_query.edit_message_text(text=end_of_day_message)


def mini_break(update, context):
    update.callback_query.answer('Понял, жду возвращения')
    mini_break_message = f'Объявлен мини-перерыв, жду возвращения'
    update.callback_query.edit_message_text(text=mini_break_message)

def rest(update, context):
    def print_return_to_workspace_dialogue(mybot):
        mybot.job_queue.run_once(callback=return_to_workspace_message, when=1)

    update.callback_query.answer('Понял, жду возвращения')
    mini_break_message = f'Объявлен мини-перерыв, жду возвращения'
    update.callback_query.edit_message_text(text=mini_break_message)
