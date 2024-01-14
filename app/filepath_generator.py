from datetime import datetime
from pathlib import Path
import os
import re


class FilepathGenerator:

    def __init__(self, source_filepath, destination_root_directory):
        self.source_filepath = source_filepath
        self.destination_root_directory = destination_root_directory
        self.spacer = '___'

    def generate_destination_filepath(self):
        filename = Path(self.source_filepath).name
        media_capture_time = self._approximate_media_capture_time()
        quarter = self.__determine_quarter(media_capture_time.month)
        prospective_destination_filepath = os.path.join(
            self.destination_root_directory, str(media_capture_time.year), quarter, filename)
        return self.__resolve_path(prospective_destination_filepath)

    def _approximate_media_capture_time(self):
        file_metadata = Path(self.source_filepath).stat()
        return datetime.fromtimestamp(min(file_metadata.st_mtime,
                                          file_metadata.st_birthtime,
                                          file_metadata.st_ctime))

    def __determine_quarter(self, month):
        quarters = {1: 'Q1', 2: 'Q1', 3: 'Q1', 4: 'Q2', 5: 'Q2', 6: 'Q2',
                    7: 'Q3', 8: 'Q3', 9: 'Q3', 10: 'Q4', 11: 'Q4', 12: 'Q4'}
        return quarters.get(month)

    def __resolve_path(self, destination_filepath):
        if not self.__path_in_use(destination_filepath):
            return destination_filepath
        if self.__destination_and_source_files_are_same_size(destination_filepath):
            return None
        else:
            return self.__generate_next_available_path(destination_filepath)

    def __path_in_use(self, path):
        return Path(path).is_file()

    def __destination_and_source_files_are_same_size(self, destination_filepath):
        return Path(self.source_filepath).stat().st_size == Path(destination_filepath).stat().st_size

    def __generate_next_available_path(self, destination_filepath):
        path = Path(destination_filepath)
        filename = self.__distinct_filename(path.stem)
        next_path = os.path.join(path.parent, filename + path.suffix)
        return self.__resolve_path(next_path) if self.__path_in_use(next_path) else next_path

    def __distinct_filename(self, filename):
        distinct_filename = f'{filename}{self.spacer}1'
        return self.__increment_suffix_number(filename) if self.__has_suffix_already(filename) \
            else distinct_filename

    def __increment_suffix_number(self, filename):
        filename, existing_suffix_number = filename.rsplit(self.spacer, 1)
        incremented_suffix_number = int(existing_suffix_number) + 1
        return f'{filename}{self.spacer}{incremented_suffix_number}'

    def __has_suffix_already(self, filename):
        return bool(re.search(self.spacer, filename))
