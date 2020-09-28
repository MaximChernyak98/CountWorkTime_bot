# pip import
import cv2.cv2 as cv2

# files import
from utils.get_frame import get_frame
from utils.start_caption import start_caption_frame


def main():
    face_cascade, videostream_for_caption = start_caption_frame()
    while True:
        frame = get_frame(face_cascade, videostream_for_caption)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    videostream_for_caption.release()


if __name__ == '__main__':
    main()
