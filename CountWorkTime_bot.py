import logging

from telegram.ext import (
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
    CommandHandler
)

from utils import (
    search_faces_in_frames,
    start_caption_frame,
    count_job_detection,
    count_work_intervals,
    set_states_current_iteration
)

from handlers import (
    greeting,
    rest_message,
    print_rest_fallback,
    end_of_day,
    mini_break,
    current_result_of_day,
    cheat_code
)

from rest_handlers import full_rest, part_rest, count_rest_part
from settings import MYBOT
from dialogues import send_end_of_day_message

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename="bot.log"
)


def main():
    dp = MYBOT.dispatcher

    rest_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(rest_message, pattern='^(rest|work|dinner)$')],
        states={'wait_answer': [CallbackQueryHandler(full_rest, pattern='full_rest'),
                                CallbackQueryHandler(part_rest, pattern='partial_rest')],
                'get_percent': [MessageHandler(Filters.regex('^\d+$'), count_rest_part)]
                },
        fallbacks=[MessageHandler(Filters.all, print_rest_fallback)]
    )

    number_job_detection = 0
    states_from_previous_iteration = {'start_work': False, 'man_at_work': False}
    face_cascade, video_for_caption = start_caption_frame()

    while True:
        number_of_face_occurrences = search_faces_in_frames(face_cascade, video_for_caption)
        number_job_detection = count_job_detection(number_of_face_occurrences, number_job_detection)
        count_work_intervals(states_from_previous_iteration)

        dp.add_handler(CommandHandler('Start', greeting))
        dp.add_handler(CommandHandler('Cheat', cheat_code))
        dp.add_handler(CallbackQueryHandler(end_of_day, pattern='end_workday'))
        dp.add_handler(CallbackQueryHandler(mini_break, pattern='mini_break'))
        dp.add_handler(MessageHandler(Filters.regex('^(Завершить работу)$'), end_of_day))
        dp.add_handler(MessageHandler(Filters.regex('^(Результаты дня)$'), current_result_of_day))
        dp.add_handler(rest_conversation)

        MYBOT.start_polling()
        states_from_previous_iteration = set_states_current_iteration(states_from_previous_iteration)


if __name__ == '__main__':
    main()
