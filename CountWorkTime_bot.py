import cv2

from utils import get_frame, start_caption_frame


def main():
    face_cascade, videostream_for_caption = start_caption_frame()
    while True:
        frame, face_increment = get_frame(face_cascade, videostream_for_caption)
        face_counter += face_increment
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    videostream_for_caption.release()


if __name__ == '__main__':
    main()
