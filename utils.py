import os
from datetime import datetime, timedelta
import cv2
import sys

import settings
import dialogues


def start_caption_frame():
    current_dir = os.path.dirname(__file__)
    face_cascade_xml = 'haarcascade_frontalface_default.xml'
    path_to_face_cascade = os.path.join(current_dir, 'cascades', face_cascade_xml)
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


def count_work_intervals(states_from_previous_iteration):
    if (not states_from_previous_iteration['start_work']) and settings.IS_WORKDAY_STARTED:
        settings.LAST_TIME_STAMP = datetime.now()
        dialogues.print_first_message()
    if states_from_previous_iteration['start_work']:
        # only if man return to workplace
        if (not states_from_previous_iteration['man_at_work']) and settings.IS_MAN_AT_WORKPLACE:
            calculate_period_time(is_return_from_break=True)
            settings.LAST_TIME_STAMP = datetime.now()
            dialogues.send_return_to_workspace_message()
        # only if man go for break
        if states_from_previous_iteration['man_at_work'] and not settings.IS_MAN_AT_WORKPLACE:
            dialogues.send_left_from_workspace_message()
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
        settings.RAW_BREAK_TIME = period_time
    else:
        period_time += timedelta(seconds=settings.SECONDS_TO_START_WORK)
        settings.SUMMARY_WORK_TIME += period_time


def timedelta_to_time_string(timedelta_period, full_format):
    days, seconds = timedelta_period.days, timedelta_period.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if full_format:
        result_string = f'{hours} часов, {minutes} минут, {seconds} секунд'
    else:
        result_string = f'{hours}:{minutes}:{seconds}'
    return result_string


def prepare_part_time_for_print(percent):
    first_part_time = settings.RAW_BREAK_TIME * percent / 100
    second_part_time = settings.RAW_BREAK_TIME * (100 - percent) / 100
    first_part_message = timedelta_to_time_string(first_part_time, full_format=True)
    second_part_message = timedelta_to_time_string(second_part_time, full_format=True)
    return first_part_time, first_part_message, second_part_time, second_part_message
