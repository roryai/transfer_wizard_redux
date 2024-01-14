from functools import partial
import os

PHOTO_EXTENSIONS = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic']
VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc']
MEDIA_EXTENSIONS = [ext.upper() for extensions in [PHOTO_EXTENSIONS, VIDEO_EXTENSIONS] for ext in extensions] \
                   + PHOTO_EXTENSIONS + VIDEO_EXTENSIONS


class Scanner:
    def media_filepaths_in(self, source_root_directory):
        return self.__scan_directory(source_root_directory, self.__media_extension, self.__full_file_path)

    def misc_extensions_in(self, source_root_directory):
        return set(self.__scan_directory(source_root_directory, self.__misc_extension, self.__extension_only))

    def __media_extension(self, filepath):
        return self.__extension(filepath) in MEDIA_EXTENSIONS

    def __misc_extension(self, extension):
        return extension not in MEDIA_EXTENSIONS

    def __extension(self, filepath):
        return os.path.splitext(filepath)[1]

    def __full_file_path(self, source_directory, filename):
        return os.path.join(source_directory, filename)

    def __extension_only(self, _, filename):
        return self.__extension(filename)

    def __scan_directory(self, source_root_directory, extension_filter, path_constructor):
        file_tree = os.walk(source_root_directory)
        for (_, _, filenames) in file_tree:
            yield from filter(extension_filter, map(partial(path_constructor, source_root_directory), filenames))
