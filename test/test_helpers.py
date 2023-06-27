import os


source_dir = "/Users/rory/code/transfer_wizard_redux/test/media/source/"
target_dir = "/Users/rory/code/transfer_wizard_redux/test/media/target/"

DESIRED_PHOTO_EXTENSIONS = ['.bmp', '.gif', '.jpg', '.jpeg', '.png', '.tif', '.tiff']


def desired_source_filepaths():
    files = []
    for ext in DESIRED_PHOTO_EXTENSIONS:  # TODO use list comprehension here
        files.append(source_dir + 'a_file' + ext)
    return sorted(files)


def create_desired_source_files():
    for file_path in desired_source_filepaths():
        open(file_path, 'x').close()


def delete_files_in(directory):
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))


def filenames_in_directory(directory):
    files = []
    for (_, _, filenames) in os.walk(directory):
        files.extend(filenames)
        break
    return sorted(files)


def create_file_with_data(directory, filename, data=''):
    file_path = directory + filename
    file = open(file_path, 'x')
    file.write(data)
    file.close()
    return file_path


def create_file(directory, filename):
    return create_file_with_data(directory, filename)

