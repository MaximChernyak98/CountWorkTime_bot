# pip import
import cv2.cv2 as cv2

# files import
from utils.get_image import get_frame
from utils.start_caption import start_caption


def main():
    face_cascade, caption_picture = start_caption()
    while True:
        frame = get_frame(caption_picture, face_cascade)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    caption_picture.release()


if __name__ == '__main__':
    main()
