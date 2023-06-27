import os

PHOTO_EXTENSIONS = ['.bmp', '.gif', '.jpg', '.jpeg', '.png', '.tif', '.tiff']


class Scanner:

    def scan_dirs(self, source_dir):
        file_tree = os.walk(source_dir)
        return self.filepaths_with_matching_extensions(file_tree)

    def filepaths_with_matching_extensions(self, file_tree):
        matching_files = []
        for (root, _, files) in file_tree:
            for file in files:
                _, extension = os.path.splitext(file)
                if extension in PHOTO_EXTENSIONS:
                    matching_files.append(root + file)
        return sorted(matching_files)
