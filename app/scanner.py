import os

PHOTO_EXTENSIONS = ['.bmp', '.gif', '.jpg', '.jpeg', '.png', '.tif', '.tiff']


class Scanner:

    def __init__(self, source_dir, target_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir

    def scan_dirs(self):
        file_tree = os.walk(self.source_dir)
        matching_files = []
        for (root, dirs, files) in file_tree:
            for file in files:
                filename, extension = os.path.splitext(file)
                if extension in PHOTO_EXTENSIONS:
                    matching_files.append(root + file)
        return matching_files
