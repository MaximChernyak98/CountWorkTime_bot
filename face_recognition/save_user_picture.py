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

def save_images_from_camera(face_cascade, video_for_caption, number_of_frame):
    current_dir = os.path.dirname(__file__)
    ret, frame = video_for_caption.read()
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # frame_roi = frame[y:y + h, x:x + w]
                img_name = f'{number_of_frame}.png'
                path_to_image = os.path.join(current_dir, 'images', img_name)
                number_of_frame += 1
                try:
                    cv2.imwrite(path_to_image, frame) # , frame_roi
                    print('Записал')
                except FileExistsError:
                    print(f'Ошибка записи, файл с имененем {img_name} существует')
                return number_of_frame
    except cv2.error as e:
        if e.err == "!_src.empty()":
            return number_of_frame
            sys.exit('Видеопоток не найден, проверьте подключение камеры')



def main():
    face_cascade, video_for_caption = start_caption_frame()
    number_of_frame = 0
    while True:
        number_of_frame = save_images_from_camera(face_cascade, video_for_caption, number_of_frame)



if __name__ == '__main__':
    main()
