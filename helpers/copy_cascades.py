import cv2
from os import path, listdir, makedirs
from shutil import copytree, copy2

path_to_cv2 = cv2.__file__
path_to_data = path.join(path.dirname(path_to_cv2), 'data')
base_path = path.dirname(__file__)
path_to_copy = path.join(base_path, 'cascades')

if not path.exists(path_to_copy):
    makedirs(path_to_copy)

def copy_directory(source, distanation, symlinks=False, ignore=None):
    for item in listdir(source):
        try:
            source_file = path.join(source, item)
            distanation_file = path.join(distanation, item)
            if path.isdir(source_file):
                copytree(source_file, distanation_file, symlinks, ignore)
            else:
                copy2(source_file, distanation_file)
        except FileExistsError:
            continue

copy_directory(path_to_data, path_to_copy)
