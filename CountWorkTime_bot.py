import cv2
import logging, datetime

from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)

from utils import (
    search_faces_in_frames,
    start_caption_frame,
    count_job_detection,
    count_work_intervals,
    set_states_current_iteration
)

import handlers
import settings
import config
import dialogues


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename="bot.log"
)


def main():
    dp = settings.MYBOT.dispatcher

    number_job_detection = 0
    states_from_previous_iteration = {'start_work': False, 'man_at_work': False}

    face_cascade, video_for_caption = start_caption_frame()

    while True:
        number_of_face_occurrences = search_faces_in_frames(face_cascade, video_for_caption)
        number_job_detection = count_job_detection(number_of_face_occurrences, number_job_detection)
        count_work_intervals(states_from_previous_iteration)

        dp.add_handler(CallbackQueryHandler(handlers.end_of_day, pattern='end_workday'))
        dp.add_handler(CallbackQueryHandler(handlers.mini_break, pattern='mini_break'))
        dp.add_handler(CallbackQueryHandler(dialogues.rest_message, pattern='rest'))

        settings.MYBOT.start_polling()
        states_from_previous_iteration = set_states_current_iteration(states_from_previous_iteration)


if __name__ == '__main__':
    main()
