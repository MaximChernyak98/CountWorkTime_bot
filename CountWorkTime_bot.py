import cv2

from utils import (
    search_faces_in_frames,
    start_caption_frame,
    count_job_detection,
    count_work_intervals,
    set_states_current_iteration
)
import settings


def main():
    number_job_detection = 0
    states_from_previous_iteration = {'start_work': False, 'man_at_work': False}

    face_cascade, video_for_caption = start_caption_frame()

    while True:
        number_of_face_occurrences = search_faces_in_frames(face_cascade, video_for_caption)
        number_job_detection = count_job_detection(number_of_face_occurrences, number_job_detection)
        count_work_intervals(states_from_previous_iteration)
        states_from_previous_iteration = set_states_current_iteration(states_from_previous_iteration)
        print(f'Work - {settings.SUMMARY_WORK_TIME}, rest - {settings.SUMMARY_BREAK_TIME}')
        print(states_from_previous_iteration)


if __name__ == '__main__':
    main()
