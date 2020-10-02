import os
import datetime
import cv2

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
            print(start_coord_x, start_coord_y, width, hieght)
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


def is_man_at_work(number_of_face_occurrences, number_of_hits_to_start):
    if number_of_face_occurrences != 0:
        number_of_hits_to_start += 1
        if number_of_hits_to_start > 10:
            number_of_hits_to_start = 10
            return True, number_of_hits_to_start
        return False, number_of_hits_to_start
    else:
        number_of_hits_to_start -= 1
        if number_of_hits_to_start < 0:
            number_of_hits_to_start = 0
            return False, number_of_hits_to_start
        return True, number_of_hits_to_start
