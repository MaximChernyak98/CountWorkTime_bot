import os
from datetime import datetime, timedelta
import cv2

import globals

current_dir = os.path.dirname(__file__)
face_cascade_xml = 'haarcascade_frontalface_default.xml'

path_to_face_cascade = os.path.join(
    current_dir,
    'cascades',
    'data',
    face_cascade_xml
)


def start_caption_frame():
    face_cascade = None
    try:
        face_cascade = cv2.CascadeClassifier(path_to_face_cascade)
    except FileNotFoundError:
        print('Файл с шаблонами не найден')
    video_capture = cv2.VideoCapture(0)
    return face_cascade, video_capture


def search_faces_in_frames(face_cascade, videostream_for_caption):
    number_of_face_occurrences = 0
    end_capture_time = datetime.now() + timedelta(seconds=1)
    while datetime.now() < end_capture_time:
        ret, frame = videostream_for_caption.read()
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
            if faces != ():
                number_of_face_occurrences += 1
        except cv2.error as e:
            if e.err == "!_src.empty()":
                print('Видеопоток не найден, проверьте подключение камеры')
                return 0
    return number_of_face_occurrences


def count_hits_at_workplace(number_of_face_occurrences, number_of_hits):
    if number_of_face_occurrences > 0:
        number_of_hits += 1
        if number_of_hits > globals.HITS_TO_START_WORK:
            number_of_hits = globals.HITS_TO_BREAK
            globals.IS_MAN_AT_WORKPLACE = True
            if globals.IS_WORKDAY_STARTED:
                globals.IS_BREAK = False
            if not globals.IS_WORKDAY_STARTED:
                globals.IS_WORKDAY_STARTED = True
    else:
        number_of_hits -= 1
        if number_of_hits < 0:
            globals.IS_MAN_AT_WORKPLACE = False
            number_of_hits = 0
            if globals.IS_WORKDAY_STARTED:
                globals.IS_BREAK = True
    return number_of_hits


def count_work_intervals(states_from_previous_iteration):
    if (not states_from_previous_iteration['start_work']) and globals.IS_WORKDAY_STARTED:
        globals.LAST_TIME_STAMP = datetime.now()
    if states_from_previous_iteration['start_work']:
        # only if man return to workplace
        if (not states_from_previous_iteration['man_at_work']) and globals.IS_MAN_AT_WORKPLACE:
            calculate_period_time(is_return_from_break=True)
            globals.LAST_TIME_STAMP = datetime.now()
        # only if man go for break
        if (not states_from_previous_iteration['break']) and globals.IS_BREAK:
            calculate_period_time(is_return_from_break=False)
            globals.LAST_TIME_STAMP = datetime.now()


def set_states_current_iteration(states_from_previous_iteration):
    states_from_previous_iteration['start_work'] = globals.IS_WORKDAY_STARTED
    states_from_previous_iteration['man_at_work'] = globals.IS_MAN_AT_WORKPLACE
    states_from_previous_iteration['break'] = globals.IS_BREAK
    return states_from_previous_iteration


def calculate_period_time(is_return_from_break):
    period_time = datetime.now() - globals.LAST_TIME_STAMP
    if is_return_from_break:
        period_time += timedelta(seconds=globals.HITS_TO_BREAK)
        globals.SUMMARY_BREAK_TIME += period_time
    else:
        period_time += timedelta(seconds=globals.HITS_TO_START_WORK)
        globals.SUMMARY_WORK_TIME += period_time
