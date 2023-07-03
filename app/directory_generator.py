from datetime import datetime
import os
from pathlib import Path
import re


class DirectoryGenerator:

    def prepare_target_path(self, source_filepath, target_directory, filename):
        decimal_birthtime = os.stat(source_filepath).st_birthtime
        birthtime = datetime.fromtimestamp(decimal_birthtime)
        quarter = self.__determine_quarter(birthtime.month)
        prospective_path = f'{target_directory}{birthtime.year}/{quarter}/{filename}'

        return self.__detect_duplicates(source_filepath, prospective_path)

    def __detect_duplicates(self, source_filepath, target_filepath):
        if not self.__path_in_use(target_filepath):
            self.__create_directory(target_filepath)
            return target_filepath
        if self.__files_are_same_size(source_filepath, target_filepath):
            return ''
        else:
            return self.__generate_next_available_path(source_filepath, target_filepath)

    def __create_directory(self, target_filepath):  # TODO refactor this away to another class
        path = Path(target_filepath)
        Path(path.parent).mkdir(parents=True, exist_ok=True)

    def __generate_next_available_path(self, source_filepath, target_filepath):
        path = Path(target_filepath)
        filename = self.__add_suffix(path.stem)
        incremented_path = f'{path.parent}/{filename}{path.suffix}'
        if self.__path_in_use(incremented_path):
            return self.__detect_duplicates(source_filepath, incremented_path)
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

    def __files_are_same_size(self, path_1, path_2):
        return os.stat(path_1).st_size == os.stat(path_2).st_size

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
