import cv2

from utils import (
    search_faces_in_frames,
    start_caption_frame,
    count_hits_at_workplace,
    count_work_intervals,
    set_states_current_iteration
)
import globals


def main():
    face_cascade, videostream_for_caption = start_caption_frame()
    number_of_hits = 0

    states_from_previous_iteration = {'start_work': False, 'man_at_work': False, 'break': False}
    while True:
        number_of_face_occurrences = search_faces_in_frames(face_cascade, videostream_for_caption)
        number_of_hits = count_hits_at_workplace(number_of_face_occurrences, number_of_hits)
        count_work_intervals(states_from_previous_iteration)
        states_from_previous_iteration = set_states_current_iteration(states_from_previous_iteration)
        print(f'Work - {globals.SUMMARY_WORK_TIME}, rest - {globals.SUMMARY_BREAK_TIME}')
        print(states_from_previous_iteration)
    videostream_for_caption.release()


if __name__ == '__main__':
    main()
