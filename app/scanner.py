from functools import partial
import os

VALID_PHOTO_EXTENSIONS = ['.bmp', '.gif', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic']
VALID_VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc']
upper_case_extensions = \
    [ext.upper() for extensions in [VALID_PHOTO_EXTENSIONS, VALID_VIDEO_EXTENSIONS] for ext in extensions]
MEDIA_EXTENSIONS = VALID_PHOTO_EXTENSIONS + VALID_VIDEO_EXTENSIONS + upper_case_extensions


class Scanner:

    def media_filepaths_in(self, source_root_directory):
        return self.__scan_directory(source_root_directory, self.__media_extension, self.__full_file_path)

    def misc_extensions_in(self, source_root_directory):
        return set(self.__scan_directory(source_root_directory, self.__misc_extension, self.__extension_only))

    def __media_extension(self, file):
        return self.__extension(file) in MEDIA_EXTENSIONS

    def __misc_extension(self, ext):
        return ext not in MEDIA_EXTENSIONS

    def __extension(self, file):
        return os.path.splitext(file)[1]

    def __full_file_path(self, root, file):
        return os.path.join(root, file)

    def __extension_only(self, _, file):
        return self.__extension(file)

    def __scan_directory(self, source_root_directory, extension_filter, path_constructor):
        file_tree = os.walk(source_root_directory)
        for (root, _, files) in file_tree:
            yield from filter(extension_filter, map(partial(path_constructor, root), files))
