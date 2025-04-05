from functools import partial
import os
from pathlib import Path

from app.filetype_constants import extension_in_media_filetypes


class Scanner:
    def media_filepaths_in(self, source_root_directory):
        return self._scan_directory(source_root_directory,
                                    self._is_filepath_of_media_filetype, self._full_file_path)

    def _is_filepath_of_media_filetype(self, filepath):
        return extension_in_media_filetypes(self._extension(filepath))

    def _extension(self, filepath):
        return Path(filepath).suffix

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
