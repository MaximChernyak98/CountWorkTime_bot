import logging

from telegram.ext import (
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
    CommandHandler
)

from helpers.utils import (
    search_faces_in_frames,
    start_caption_frame,
    count_job_detection,
    count_work_intervals,
    set_states_current_iteration
)

from interaction.handlers import (
    greeting,
    rest_message,
    print_rest_fallback,
    end_of_day,
    mini_break,
    current_result_of_day,
    cheat_code
)

from interaction.rest_handlers import (
    count_rest_part,
    full_rest,
    part_rest
)

from interaction.rest_conversation import rest_conversation, set_pomadoro_conversation
from settings import MYBOT
import initialization

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename="bot.log"
)


def main():
    dp = MYBOT.dispatcher
    initialization.initialization(dp)

    number_job_detection = 0
    states_from_previous_iteration = {'start_work': False, 'man_at_work': False}
    face_cascades, video_for_caption = start_caption_frame()

    while True:
        number_of_face_occurrences = search_faces_in_frames(face_cascades, video_for_caption)
        number_job_detection = count_job_detection(number_of_face_occurrences, number_job_detection)
        count_work_intervals(states_from_previous_iteration)

        dp.add_handler(CommandHandler('Start', greeting))
        dp.add_handler(CommandHandler('Cheat', cheat_code))
        dp.add_handler(CallbackQueryHandler(end_of_day, pattern='end_workday'))
        dp.add_handler(CallbackQueryHandler(mini_break, pattern='mini_break'))
        dp.add_handler(MessageHandler(Filters.regex('^(Завершить работу)$'), end_of_day))
        dp.add_handler(MessageHandler(Filters.regex('^(Результаты дня)$'), current_result_of_day))

        dp.add_handler(rest_conversation)
        dp.add_handler(set_pomadoro_conversation)

        states_from_previous_iteration = set_states_current_iteration(states_from_previous_iteration)


if __name__ == '__main__':
    main()
