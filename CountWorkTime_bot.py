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
    intervals_list = []
    states_from_previous_iteration = {'start work?': False, 'man at work?': False, 'break?': False}
    while True:
        number_of_face_occurrences = search_faces_in_frames(face_cascade, videostream_for_caption)
        number_of_hits = count_hits_at_workplace(number_of_face_occurrences, number_of_hits)
        intervals_list = count_work_intervals(intervals_list, states_from_previous_iteration)
        states_from_previous_iteration = set_states_current_iteration(states_from_previous_iteration)
        print(intervals_list)
    videostream_for_caption.release()


if __name__ == '__main__':
    main()
