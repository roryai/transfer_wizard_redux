from pathlib import Path
import os
import re

from app.capture_date_identifier import CaptureDateIdentifier
from app.file import File
from app.file_gateway import FileGateway
from app.logger import Logger
from app.mode_flags import ModeFlags


class FilepathGenerator:

    def __init__(self, source_filepath, destination_root_directory):
        self.source_filepath = source_filepath
        self.destination_root_directory = destination_root_directory
        self.gateway = FileGateway()
        self.spacer = '___'

    def generate_destination_filepath(self):
        filename = Path(self.source_filepath).name
        capture_date = CaptureDateIdentifier().media_capture_date(self.source_filepath)
        quarter = self._determine_quarter(capture_date.month)
        prospective_destination_filepath = os.path.join(
            self.destination_root_directory, str(capture_date.year), quarter, filename)
        return self._resolve_path(prospective_destination_filepath)

    def _determine_quarter(self, month):
        if ModeFlags().year_mode:
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
        return Path(path).is_file() or self.gateway.destination_filepath_in_use(path)

    def _destination_and_source_files_are_same_size(self, destination_filepath):
        if self._identical_record_exists_for_file(destination_filepath):
            record = self.gateway.select_duplicate_file(
                destination_filepath, self._source_file_size())
            duplicate_source_path = File.init_from_record(record).source_filepath
            Logger().log_duplicate(self.source_filepath, duplicate_source_path)
            return True
        if os.path.exists(destination_filepath):
            return self._source_file_size() == Path(destination_filepath).stat().st_size
        else:
            return False

    def _identical_record_exists_for_file(self, destination_filepath):
        return self.gateway.identical_size_and_destination_filepath_record_exists(destination_filepath,
                                                                                  self._source_file_size())

    def _source_file_size(self):
        return Path(self.source_filepath).stat().st_size

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
