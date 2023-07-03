from datetime import datetime
import os
from pathlib import Path
import re


class FilepathGenerator:

    def __init__(self, source_filepath, target_directory):
        self.source_filepath = source_filepath
        self.target_directory = target_directory

    def generate_target_filepath(self):
        filename = Path(self.source_filepath).name
        file_birthtime = datetime.fromtimestamp(os.stat(self.source_filepath).st_birthtime)
        quarter = self.__determine_quarter(file_birthtime.month)
        prospective_target_filepath = f'{self.target_directory}{file_birthtime.year}/{quarter}/{filename}'

        return self.__detect_duplicates(prospective_target_filepath)

    def __detect_duplicates(self, target_filepath):
        if not self.__path_in_use(target_filepath):
            return target_filepath
        if self.__target_and_source_files_are_same_size(target_filepath):
            return ''
        else:
            return self.__generate_next_available_path(target_filepath)

    def __generate_next_available_path(self, target_filepath):
        path = Path(target_filepath)
        filename = self.__add_suffix(path.stem)
        incremented_path = f'{path.parent}/{filename}{path.suffix}'
        if self.__path_in_use(incremented_path):
            return self.__detect_duplicates(incremented_path)
        else:
            return incremented_path

    def __add_suffix(self, filename):
        if bool(re.search("___", filename)):
            return self.__increment_suffix_number(filename)
        else:
            return filename + '___1'

    def __increment_suffix_number(self, filename):
        filename, existing_number_suffix = filename.rsplit('___', 1)
        number_suffix = str(int(existing_number_suffix) + 1)
        return filename.rsplit('___', 1)[0] + '___' + number_suffix

    def __path_in_use(self, path):
        return os.path.isfile(path)

    def __target_and_source_files_are_same_size(self, target_filepath):
        return os.stat(self.source_filepath).st_size == os.stat(target_filepath).st_size

    def __determine_quarter(self, month):
        match month:
            case 1 | 2 | 3:
                return 'Q1'
            case 4 | 5 | 6:
                return 'Q2'
            case 7 | 8 | 9:
                return 'Q3'
            case 10 | 11 | 12:
                return 'Q4'
            case _:
                raise TypeError
