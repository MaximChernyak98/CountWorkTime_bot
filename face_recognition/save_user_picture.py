from datetime import datetime, timedelta
import os

import cv2

from utils import (
    search_faces_in_frames,
    start_caption_frame,
    count_job_detection,
    count_work_intervals,
    set_states_current_iteration
)

current_dir = os.path.dirname(__file__)


def search_faces_in_frames(face_cascade, video_for_caption, number_of_frame):
    ret, frame = video_for_caption.read()
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                frame_roi = frame[y:y + h, x:x + w]
                img_name = f'{number_of_frame}.png'
                path_to_image = os.path.join(current_dir, 'images', img_name)
                number_of_frame += 1
                try:
                    cv2.imwrite(path_to_image, frame_roi)
                except FileExistsError:
                    print(f'Ошибка записи, файл с имененем {img_name} существует')
    except cv2.error as e:
        if e.err == "!_src.empty()":
            sys.exit('Видеопоток не найден, проверьте подключение камеры')
    return number_of_frame


def main():
    face_cascade, video_for_caption = start_caption_frame()
    number_of_frame = 0
    while True:
        number_of_frame = search_faces_in_frames(face_cascade, video_for_caption, number_of_frame)
        print(number_of_frame)


if __name__ == '__main__':
    main()
