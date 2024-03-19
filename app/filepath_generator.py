from pathlib import Path
import os
import re

from app.capture_time_identifier import CaptureTimeIdentifier
from app.mode_flags import ModeFlags


class FilepathGenerator:

    def __init__(self, source_filepath, destination_root_directory,
                 et,
                 capture_time_identifier=CaptureTimeIdentifier()):
        self.source_filepath = source_filepath
        self.destination_root_directory = destination_root_directory
        self.misc_root_directory = os.path.join(destination_root_directory, 'misc')
        self.capture_time_identifier = capture_time_identifier
        self.spacer = '___'

    def generate_destination_filepath(self, media):
        filename = Path(self.source_filepath).name
        result = self.capture_time_identifier.approximate_file_creation_date(self.source_filepath, self.et)
        capture_date = result['capture_date']
        quarter = self._determine_quarter(capture_date.month, media)
        root = self._root_dir(media, result['metadata_unreadable'])
        prospective_destination_filepath = os.path.join(
            root, str(capture_date.year), quarter, filename)
        return self._resolve_path(prospective_destination_filepath)

    def _determine_quarter(self, month, media):
        if ModeFlags().year_mode or not media:
            return ''
        quarters = {1: 'Q1', 2: 'Q1', 3: 'Q1', 4: 'Q2', 5: 'Q2', 6: 'Q2',
                    7: 'Q3', 8: 'Q3', 9: 'Q3', 10: 'Q4', 11: 'Q4', 12: 'Q4'}
        return quarters.get(month)

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

    def _root_dir(self, media, metadata_unreadable):
        root = self.destination_root_directory if media else self.misc_root_directory
        if metadata_unreadable:
            root = os.path.join(root, 'error')
        return root
