import os
import cv2
import numpy as np
from PIL import Image
import pickle

current_dir = os.path.dirname(__file__)
path_to_images = os.path.join(current_dir, 'images')

current_dir = os.path.dirname(__file__)
face_cascade_xml = 'haarcascade_frontalface_default.xml'
path_to_face_cascade = os.path.join(current_dir, '..', 'cascades', face_cascade_xml)
face_cascade = cv2.CascadeClassifier(path_to_face_cascade)
recognizer = cv2.face.LBPHFaceRecognizer_create()


def train_face_recognition(path_to_images):
    x_train = []
    y_user_name_id = []
    labels_id = {}
    current_id = 0
    for root, dirs, files in os.walk(path_to_images):
        for file in files:
            if file.endswith('png') or file.endswith('jpg'):
                path_to_file = os.path.join(root, file)
                user_name = os.path.basename(root).replace(' ', '-')
                if user_name not in labels_id:
                    labels_id[user_name] = current_id
                    current_id += 1
                id_ = labels_id[user_name]
                pil_image = Image.open(path_to_file).convert('L')  # convert to grayscale
                size = (800,800)
                final_image = pil_image.resize(size, Image.ANTIALIAS)
                image_array = np.array(final_image, 'uint8')
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
                for (x, y, w, h) in faces:
                    frame_roi = image_array[y:y + h, x:x + w]
                    x_train.append(frame_roi)
                    y_user_name_id.append(id_)
    return x_train, y_user_name_id, labels_id


def main():
    x_train, y_user_name_id, labels_id = train_face_recognition(path_to_images)
    print(y_user_name_id)
    recognizer.train(x_train, np.array(y_user_name_id))
    recognizer.save('trainner.yml')

    with open('labels.pickle', 'wb') as f:
        pickle.dump(labels_id, f)


if __name__ == '__main__':
    main()
