# pip import
# import numpy as np
import cv2.cv2 as cv2


def get_frame(caption_video, face_cascade):
    # Capture frame-by-frame
    ret, frame = caption_video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        end_coordinate_x = x + w
        end_coordinate_y = y + h

        # img_item = 'my-image.png'
        # cv2.imwrite(img_item, roi_color)

        # settings for ROI
        roi_gray = gray[y:end_coordinate_y, x:end_coordinate_x]
        roi_color = frame[y:end_coordinate_y, x:end_coordinate_x]
        color = (255, 0, 0)  # BGR
        stroke = 2

        cv2.rectangle(frame, (x, y),
                      (end_coordinate_x, end_coordinate_y),
                      color, stroke)
    return frame
