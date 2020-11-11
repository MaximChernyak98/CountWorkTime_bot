import os
from datetime import datetime, timedelta
import cv2
import sys

import settings

from helpers.timedelta_to_str import timedelta_to_time_string

from interaction.dialogues import (
    print_first_message,
    send_return_to_workspace_message,
    send_left_from_workspace_message
)


def get_paths_to_face_cascades(dir: str):
    list_of_face_cascades = [
        'haarcascade_frontalface_default.xml', 'haarcascade_profileface.xml']
    paths_to_face_cascades = []
    for cascade in list_of_face_cascades:
        path_to_current_cascade = os.path.join(dir, 'cascades', cascade)
        if os.path.isfile(path_to_current_cascade):
            paths_to_face_cascades.append(path_to_current_cascade)
        else:
            print(f'Файл с шаблоном {cascade} не найден')
    return paths_to_face_cascades


def start_caption_frame():
    current_dir = os.getcwd()
    paths_to_face_cascades = get_paths_to_face_cascades(current_dir)
    face_cascades = []
    if paths_to_face_cascades:
        for path_to_cascade in paths_to_face_cascades:
            face_cascades.append(cv2.CascadeClassifier(path_to_cascade))
    else:
        sys.exit(f'Ни один файл с шаблоном не был найден, проверьте наличие папки cascades')  # TODO переделать в исключение
    video_capture = cv2.VideoCapture(0)
    return face_cascades, video_capture


def search_face_by_cascades(gray_frame, face_cascades):
    number_of_face_in_frame = 0
    for cascade in face_cascades:
        faces = cascade.detectMultiScale(gray_frame, scaleFactor=1.5, minNeighbors=5)
        if len(faces) > 0:
            number_of_face_in_frame += 1
    return number_of_face_in_frame


def search_faces_in_frames(face_cascades, video_for_caption):
    number_of_face_occurrences = 0
    end_capture_time = datetime.now() + timedelta(seconds=1)
    while datetime.now() < end_capture_time:
        ret, frame = video_for_caption.read()
        try:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            number_of_face_occurrences += search_face_by_cascades(gray_frame, face_cascades)
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
        print_first_message()
    if states_from_previous_iteration['start_work']:
        # only if man return to workplace
        if (not states_from_previous_iteration['man_at_work']) and settings.IS_MAN_AT_WORKPLACE:
            calculate_period_time(is_return_from_break=True)
            settings.LAST_TIME_STAMP = datetime.now()
            send_return_to_workspace_message()
        # only if man go for break
        if states_from_previous_iteration['man_at_work'] and not settings.IS_MAN_AT_WORKPLACE:
            send_left_from_workspace_message()
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


def prepare_part_time_for_print(percent):
    first_part_time = settings.RAW_BREAK_TIME * percent / 100
    second_part_time = settings.RAW_BREAK_TIME * (100 - percent) / 100
    first_part_message = timedelta_to_time_string(
        first_part_time, full_format=True)
    second_part_message = timedelta_to_time_string(
        second_part_time, full_format=True)
    return first_part_time, first_part_message, second_part_time, second_part_message
