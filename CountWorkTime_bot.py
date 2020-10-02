import cv2

from utils import search_faces_in_frames, start_caption_frame, is_man_at_work


def main():
    face_cascade, videostream_for_caption = start_caption_frame()

    is_man_at_work_b = False
    number_of_hits_to_start = 0
    while True:
        number_of_face_occurrences = search_faces_in_frames(face_cascade, videostream_for_caption)
        is_man_at_work_b, result_number_of_hits = is_man_at_work(number_of_face_occurrences, number_of_hits_to_start)
        number_of_hits_to_start = result_number_of_hits
        print(f'{result_number_of_hits} - человек на работе? {is_man_at_work_b}')
    videostream_for_caption.release()


if __name__ == '__main__':
    main()
