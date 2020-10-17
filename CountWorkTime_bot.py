import cv2
import logging, datetime
from telegram.ext import Updater, MessageHandler, Filters

from utils import (
    search_faces_in_frames,
    start_caption_frame,
    count_job_detection,
    count_work_intervals,
    set_states_current_iteration
)
import settings
import config
import bot_jobs

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename="bot.log"
)


def main():
    mybot = Updater(token=config.TOKEN, use_context=True)
    dp = mybot.dispatcher

    number_job_detection = 0
    states_from_previous_iteration = {'start_work': False, 'man_at_work': False}

    face_cascade, video_for_caption = start_caption_frame()

    mybot.job_queue.run_repeating(bot_jobs.send_message_to_user, interval=5)

    while True:
        number_of_face_occurrences = search_faces_in_frames(face_cascade, video_for_caption)
        number_job_detection = count_job_detection(number_of_face_occurrences, number_job_detection)
        count_work_intervals(states_from_previous_iteration)
        states_from_previous_iteration = set_states_current_iteration(states_from_previous_iteration)
        mybot.bot.send_message(chat_id=341231444, text=message)
        print(f'Work - {settings.SUMMARY_WORK_TIME}, rest - {settings.SUMMARY_BREAK_TIME}')
        print(states_from_previous_iteration)

        mybot.start_polling()

if __name__ == '__main__':
    main()
