from functools import partial
import os

PHOTO_FILETYPES = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic']
VIDEO_FILETYPES = ['.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc', '.mts']
MEDIA_FILETYPES = [ext.upper() for extensions in [PHOTO_FILETYPES, VIDEO_FILETYPES] for ext in extensions] \
                  + PHOTO_FILETYPES + VIDEO_FILETYPES


class Scanner:
    def media_filepaths_in(self, source_root_directory):
        return self._scan_directory(source_root_directory,
                                     self._is_filepath_of_media_filetype, self._full_file_path)

    def misc_filepaths_in(self, source_root_directory):
        return self._scan_directory(source_root_directory,
                                     self._is_filepath_of_misc_filetype, self._full_file_path)

    def misc_extensions_in(self, source_root_directory):
        return set(self._scan_directory(source_root_directory,
                                         self._is_extension_of_misc_filetype, self._extension_only))

    def _is_filepath_of_media_filetype(self, filepath):
        return self._extension(filepath) in MEDIA_FILETYPES

    def _is_filepath_of_misc_filetype(self, filepath):
        return self._is_extension_of_misc_filetype(self._extension(filepath))

    def _is_extension_of_misc_filetype(self, extension):
        return extension not in MEDIA_FILETYPES

    def _extension(self, filepath):
        return os.path.splitext(filepath)[1]

    def _full_file_path(self, source_directory, filename):
        return os.path.join(source_directory, filename)

    def _extension_only(self, _, filename):
        return self._extension(filename)

    def _scan_directory(self, source_root_directory, extension_filter, path_constructor):
        file_tree = os.walk(source_root_directory)
        for (root, _, files) in file_tree:
            file_paths_with_root = map(partial(path_constructor, root), files)
            filtered_file_paths = filter(extension_filter, file_paths_with_root)
            yield from filtered_file_paths

