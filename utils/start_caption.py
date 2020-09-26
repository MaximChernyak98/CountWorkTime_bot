# std import
import os

# pip import
import cv2.cv2 as cv2

# variables
current_dir = os.path.dirname(__file__)
face_cascade_xml = 'haarcascade_frontalface_default.xml'

# get path to using cascade (in any system)
path_to_face_cascade = os.path.join(current_dir,
                                    '..',
                                    'cascades',
                                    'data',
                                    face_cascade_xml)


def start_caption():
    face_cascade = cv2.CascadeClassifier(path_to_face_cascade)
    caption_picture = cv2.VideoCapture(0)
    return face_cascade, caption_picture
