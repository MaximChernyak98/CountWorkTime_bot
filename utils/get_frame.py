# pip import
# import numpy as np
import cv2.cv2 as cv2


def get_frame(face_cascade, videostream_for_caption):
    ret, frame = videostream_for_caption.read()
    # get gray frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (start_coord_x, start_coord_y, width, hieght) in faces:
        print(start_coord_x, start_coord_y, width, hieght)
        end_coordinate_x = start_coord_x + width
        end_coordinate_y = start_coord_y + hieght

        # set ROI-settings
        roi_color = (255, 0, 0)  # BGR
        roi_stroke = 2
        roi_start_point = (start_coord_x, start_coord_y)
        roi_end_point = (end_coordinate_x, end_coordinate_y)

        # add ROI to image
        cv2.rectangle(frame, roi_start_point, roi_end_point, roi_color, roi_stroke)
    return frame
