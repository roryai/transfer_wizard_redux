from datetime import datetime
from pathlib import Path as p
import re


class FilepathGenerator:

    def __init__(self, source_filepath, target_directory):
        self.source_filepath = source_filepath
        self.target_directory = self.__sanitise_filepath(target_directory)

    def generate_target_filepath(self):
        filename = p(self.source_filepath).name
        file_birthtime = self.__get_file_birthtime()
        quarter = self.__determine_quarter(file_birthtime.month)
        prospective_target_filepath = f'{self.target_directory}{file_birthtime.year}/{quarter}/{filename}'

        return self.__detect_duplicates(prospective_target_filepath)

    def __sanitise_filepath(self, filepath):
        if filepath[-1] != '/':
            filepath += '/'
        return filepath

    def __get_file_birthtime(self):
        birthtime_in_seconds = p(self.source_filepath).stat().st_birthtime
        return datetime.fromtimestamp(birthtime_in_seconds)

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

    def __detect_duplicates(self, target_filepath):
        if not self.__path_in_use(target_filepath):
            return target_filepath
        if self.__target_and_source_files_are_same_size(target_filepath):
            return ''
        else:
            return self.__generate_next_available_path(target_filepath)

    def __path_in_use(self, path):
        return p(path).is_file()

    def __target_and_source_files_are_same_size(self, target_filepath):
        return p(self.source_filepath).stat().st_size == p(target_filepath).stat().st_size

    def __generate_next_available_path(self, target_filepath):
        path = p(target_filepath)
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
