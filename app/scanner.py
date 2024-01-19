from functools import partial
import os

PHOTO_FILETYPES = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic']
VIDEO_FILETYPES = ['.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc']
MEDIA_FILETYPES = [ext.upper() for extensions in [PHOTO_FILETYPES, VIDEO_FILETYPES] for ext in extensions] \
                  + PHOTO_FILETYPES + VIDEO_FILETYPES


class Scanner:
    def media_filepaths_in(self, source_root_directory):
        return self.__scan_directory(source_root_directory,
                                     self.__is_filepath_of_media_filetype, self.__full_file_path)

    def misc_filepaths_in(self, source_root_directory):
        return self.__scan_directory(source_root_directory,
                                     self.__is_filepath_of_misc_filetype, self.__full_file_path)

    def misc_extensions_in(self, source_root_directory):
        return set(self.__scan_directory(source_root_directory,
                                         self.__is_extension_of_misc_filetype, self.__extension_only))

    def __is_filepath_of_media_filetype(self, filepath):
        return self.__extension(filepath) in MEDIA_FILETYPES

    def __is_filepath_of_misc_filetype(self, filepath):
        return self.__is_extension_of_misc_filetype(self.__extension(filepath))

    def __is_extension_of_misc_filetype(self, extension):
        return extension not in MEDIA_FILETYPES

    def __extension(self, filepath):
        return os.path.splitext(filepath)[1]

    def __full_file_path(self, source_directory, filename):
        return os.path.join(source_directory, filename)

    def __extension_only(self, _, filename):
        return self.__extension(filename)

    def __scan_directory(self, source_root_directory, extension_filter, path_constructor):
        file_tree = os.walk(source_root_directory)
        for (root, _, files) in file_tree:
            file_paths_with_root = map(partial(path_constructor, root), files)
            filtered_file_paths = filter(extension_filter, file_paths_with_root)
            yield from filtered_file_paths

