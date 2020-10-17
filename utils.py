import os
from datetime import datetime, timedelta
import cv2
import sys

import settings
import config


def start_caption_frame():
    current_dir = os.path.dirname(__file__)
    face_cascade_xml = 'haarcascade_frontalface_default.xml'
    path_to_face_cascade = os.path.join(current_dir, 'cascades', 'data', face_cascade_xml)
    if os.path.isfile(path_to_face_cascade):
        face_cascade = cv2.CascadeClassifier(path_to_face_cascade)
        video_capture = cv2.VideoCapture(0)
    else:
        sys.exit(f'Файл с шаблонами {face_cascade_xml} не найден')
    return face_cascade, video_capture


def search_faces_in_frames(face_cascade, video_for_caption):
    number_of_face_occurrences = 0
    end_capture_time = datetime.now() + timedelta(seconds=1)
    while datetime.now() < end_capture_time:
        ret, frame = video_for_caption.read()
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
            if len(faces) > 0:
                number_of_face_occurrences += 1
        except cv2.error as e:
            if e.err == "!_src.empty()":
                sys.exit('Видеопоток не найден, проверьте подключение камеры')
    return number_of_face_occurrences


def count_job_detection(number_of_face_occurrences, number_job_detection):
    if number_of_face_occurrences > 0:
        number_job_detection += 1
        if number_job_detection > settings.SECONDS_TO_START_WORK:
            number_job_detection = settings.SECONDS_TO_BREAK
            settings.IS_MAN_AT_WORKPLACE = settings.IS_WORKDAY_STARTED = True
    else:
        number_job_detection -= 1
        if number_job_detection < 0:
            settings.IS_MAN_AT_WORKPLACE = False
            number_job_detection = 0
    return number_job_detection


def count_work_intervals(states_from_previous_iteration, mybot):
    if (not states_from_previous_iteration['start_work']) and settings.IS_WORKDAY_STARTED:
        settings.LAST_TIME_STAMP = datetime.now()
        first_message = f'Вижу тебя, с началом рабочего дня!'
        mybot.bot.send_message(chat_id=config.CHAT_ID, text=first_message)
    if states_from_previous_iteration['start_work']:
        # only if man return to workplace
        if (not states_from_previous_iteration['man_at_work']) and settings.IS_MAN_AT_WORKPLACE:
            calculate_period_time(is_return_from_break=True)
            settings.LAST_TIME_STAMP = datetime.now()
        # only if man go for break
        if states_from_previous_iteration['man_at_work'] and not settings.IS_MAN_AT_WORKPLACE:
            calculate_period_time(is_return_from_break=False)
            settings.LAST_TIME_STAMP = datetime.now()


def set_states_current_iteration(states_from_previous_iteration):
    states_from_previous_iteration['start_work'] = settings.IS_WORKDAY_STARTED
    states_from_previous_iteration['man_at_work'] = settings.IS_MAN_AT_WORKPLACE
    return states_from_previous_iteration


def calculate_period_time(is_return_from_break=False):
    period_time = datetime.now() - settings.LAST_TIME_STAMP
    if is_return_from_break:
        period_time += timedelta(seconds=settings.SECONDS_TO_BREAK)
        settings.SUMMARY_BREAK_TIME += period_time
    else:
        period_time += timedelta(seconds=settings.SECONDS_TO_START_WORK)
        settings.SUMMARY_WORK_TIME += period_time
