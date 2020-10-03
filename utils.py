import os
import datetime
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
    try:
        face_cascade = cv2.CascadeClassifier(path_to_face_cascade)
    except FileNotFoundError:
        print('Файл с шаблонами не найден')
    video_capture = cv2.VideoCapture(0)
    return face_cascade, video_capture


def search_faces_in_frames(face_cascade, videostream_for_caption):
    number_of_face_occurrences = 0
    end_capture_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
    while datetime.datetime.now() < end_capture_time:
        ret, frame = videostream_for_caption.read()
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        except cv2.error as e:
            if e.err == "!_src.empty()":
                print('Видеопоток не найден, проверьте подключение камеры')
                return False, 0
        for (start_coord_x, start_coord_y, width, hieght) in faces:
            # print(start_coord_x, start_coord_y, width, hieght)
            end_coordinate_x = start_coord_x + width
            end_coordinate_y = start_coord_y + hieght

            roi_color = (255, 0, 0)  # BGR
            roi_stroke = 2
            roi_start_point = (start_coord_x, start_coord_y)
            roi_end_point = (end_coordinate_x, end_coordinate_y)

            cv2.rectangle(frame, roi_start_point, roi_end_point, roi_color, roi_stroke)
        if faces != ():
            number_of_face_occurrences += 1
    return number_of_face_occurrences


def count_hits_at_workplace(number_of_face_occurrences, number_of_hits):
    if number_of_face_occurrences > 0:
        number_of_hits += 1
        if number_of_hits > 5:
            number_of_hits = 10
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


def count_work_intervals(intervals_list, states_from_previous_iteration):
    if (not states_from_previous_iteration['start work?']) and globals.IS_WORKDAY_STARTED:
        intervals_list.append(f'{datetime.datetime.now().strftime("%H:%M:%S")} - начало работы')
    if states_from_previous_iteration['start work?']:
        # only if man return to workplace
        if (not states_from_previous_iteration['man at work?']) and globals.IS_MAN_AT_WORKPLACE:
            intervals_list.append(f'{datetime.datetime.now().strftime("%H:%M:%S")} - продолжил работу')
        # only if man go for break
        if (not states_from_previous_iteration['break?']) and globals.IS_BREAK:
            intervals_list.append(f'{datetime.datetime.now().strftime("%H:%M:%S")} - начался перерыв')
    return intervals_list


def set_states_current_iteration(states_from_previous_iteration):
    states_from_previous_iteration['start work?'] = globals.IS_WORKDAY_STARTED
    states_from_previous_iteration['man at work?'] = globals.IS_MAN_AT_WORKPLACE
    states_from_previous_iteration['break?'] = globals.IS_BREAK
    return states_from_previous_iteration
