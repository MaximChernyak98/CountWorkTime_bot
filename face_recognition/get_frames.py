# std import
import os
import pickle

# pip import
import numpy as np
import cv2

# variables
current_dir = os.path.dirname(__file__)
face_cascade_xml = 'haarcascade_frontalface_default.xml'
labels = {'person_name': 1}

with open('labels.pickle', 'rb') as f:
    labels_from_pickle = pickle.load(f)
    labels = {v: k for k, v in labels_from_pickle.items()}

# get path to using cascade (in any system)
path_to_face_cascade = os.path.join(current_dir, '..', 'cascades', face_cascade_xml)

face_cascade = cv2.CascadeClassifier(path_to_face_cascade)
recognizer = cv2.face.LBPHFaceRecognizer_create()
path_to_trainner_file = os.path.join(current_dir, 'trainner.yml')
recognizer.read(path_to_trainner_file)

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        end_coordinate_x = x + w
        end_coordinate_y = y + h
        roi_gray = gray[y:end_coordinate_y, x:end_coordinate_x]
        roi_color = frame[y:end_coordinate_y, x:end_coordinate_x]

        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45:  # if conf >= 45: #
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
        img_item = 'my-image.png'
        cv2.imwrite(img_item, roi_color)

        color = (255, 0, 0)  # BGR
        stroke = 2

        cv2.rectangle(frame, (x, y),
                      (end_coordinate_x, end_coordinate_y),
                      color, stroke)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWinows()
