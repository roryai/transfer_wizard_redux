import os

VALID_PHOTO_EXTENSIONS = ['.bmp', '.gif', '.jpg', '.jpeg', '.png', '.tif', '.tiff']


class Scanner:

    def scan_directory(self, source_dir):
        file_tree = os.walk(source_dir)
        for (root, _, files) in file_tree:
            for file in files:
                _, extension = os.path.splitext(file)
                if extension in VALID_PHOTO_EXTENSIONS:
                    yield self.__sanitise_filepath(root) + file

    def __sanitise_filepath(self, filepath):
        if filepath[-1] != '/':
            filepath += '/'
        return filepath
