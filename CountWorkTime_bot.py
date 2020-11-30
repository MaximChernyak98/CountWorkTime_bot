import logging
import time

from telegram.error import RetryAfter, TimedOut

from telegram.ext import (MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler, CommandHandler)

from helpers.utils import (search_faces_in_frames, start_caption_frame, count_job_detection,
                           count_work_intervals, set_states_current_iteration)

from interaction.handlers import (greeting, rest_message, print_rest_fallback,
                                  end_of_day, mini_break, current_result_of_day, cheat_code, switch_debug_mode)

from interaction.rest_handlers import (count_rest_part, full_rest, part_rest)

from interaction.conversations import rest_conversation, set_pomadoro_conversation

from helpers.debug_decorator import Debugger

import initialization

import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename="bot.log"
)


def main():
    dp = settings.MYBOT.dispatcher
    initialization.initialization(dp)

    number_job_detection = 0
    states_from_previous_iteration = {'start_work': False, 'man_at_work': False}
    face_cascades, video_for_caption = start_caption_frame()
    settings.DEBUG_MODE = False

    while True:
        try:
            Debugger.enabled = settings.DEBUG_MODE

            # try to find face in frames, if find - count work intervals
            number_of_face_occurrences = search_faces_in_frames(face_cascades, video_for_caption)
            number_job_detection = count_job_detection(number_of_face_occurrences, number_job_detection)
            count_work_intervals(states_from_previous_iteration)

            # process events by handlers
            dp.add_handler(CommandHandler('Start', greeting))
            dp.add_handler(CommandHandler('Cheat', cheat_code))
            dp.add_handler(CommandHandler('Switch', switch_debug_mode))
            dp.add_handler(CallbackQueryHandler(end_of_day, pattern='end_workday'))
            dp.add_handler(CallbackQueryHandler(mini_break, pattern='mini_break'))
            dp.add_handler(MessageHandler(Filters.regex('^(Завершить работу)$'), end_of_day))
            dp.add_handler(MessageHandler(Filters.regex('^(Результаты дня)$'), current_result_of_day))

            dp.add_handler(rest_conversation)
            dp.add_handler(set_pomadoro_conversation)

            # save state for detect switch work status
            states_from_previous_iteration = set_states_current_iteration(states_from_previous_iteration)
        except (RetryAfter, TimedOut) as e:
            print('TimedOut exception was handled')
            time.sleep(5)


if __name__ == '__main__':
    main()
