import os

current_dir = os.path.dirname(__file__)
dir_with_photo_to_rename = 'Николас Кейдж'
path_to_images = os.path.join(current_dir, 'images', dir_with_photo_to_rename)


def rename_images_files(path_to_images):
    files_counter = 0
    for root, dirs, files in os.walk(path_to_images):
        for file in files:
            file_list = file.split('.')
            file_extension = file_list[1]
            new_name = f'{str(files_counter)}.{file_extension}'
            old_path = root + os.path.sep + file
            new_path = root + os.path.sep + new_name
            os.rename(old_path, new_path)
            files_counter += 1


def main():
    rename_images_files(path_to_images)


if __name__ == '__main__':
    main()
