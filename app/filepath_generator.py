from datetime import datetime
from pathlib import Path
import os
import re


class FilepathGenerator:

    def __init__(self, source_filepath, destination_root_directory):
        self.source_filepath = source_filepath
        self.destination_root_directory = destination_root_directory
        self.misc_root_directory = os.path.join(destination_root_directory, 'misc')
        self.spacer = '___'

    def generate_destination_filepath(self, media):
        return self._generate_media_destination_filepath() if media \
            else self._generate_misc_destination_filepath()

    def _generate_media_destination_filepath(self):
        filename = Path(self.source_filepath).name
        media_capture_time = self._approximate_media_capture_time()
        prospective_destination_filepath = os.path.join(
            self.destination_root_directory, str(media_capture_time.year), filename)
        return self._resolve_path(prospective_destination_filepath)

    def _generate_misc_destination_filepath(self):
        filename = Path(self.source_filepath).name
        prospective_destination_filepath = os.path.join(self.misc_root_directory, filename)
        return self._resolve_path(prospective_destination_filepath)

    def _approximate_media_capture_time(self):
        file_metadata = Path(self.source_filepath).stat()
        return datetime.fromtimestamp(min(file_metadata.st_mtime,
                                          file_metadata.st_birthtime,
                                          file_metadata.st_ctime))

    def _resolve_path(self, destination_filepath):
        if not self._path_in_use(destination_filepath):
            return destination_filepath
        if self._destination_and_source_files_are_same_size(destination_filepath):
            return None
        else:
            return self._generate_next_available_path(destination_filepath)

    def _path_in_use(self, path):
        return Path(path).is_file()

    def _destination_and_source_files_are_same_size(self, destination_filepath):
        return Path(self.source_filepath).stat().st_size == Path(destination_filepath).stat().st_size

    def _generate_next_available_path(self, destination_filepath):
        path = Path(destination_filepath)
        filename = self._distinct_filename(path.stem)
        next_path = os.path.join(path.parent, f'{filename}{path.suffix}')
        return self._resolve_path(next_path) if self._path_in_use(next_path) else next_path

    def _distinct_filename(self, filename):
        distinct_filename = f'{filename}{self.spacer}1'
        return self._increment_suffix_number(filename) if self._has_suffix_already(filename) \
            else distinct_filename

    def _increment_suffix_number(self, filename):
        filename, existing_suffix_number = filename.rsplit(self.spacer, 1)
        incremented_suffix_number = int(existing_suffix_number) + 1
        return f'{filename}{self.spacer}{incremented_suffix_number}'

    def _has_suffix_already(self, filename):
        return bool(re.search(self.spacer, filename))
