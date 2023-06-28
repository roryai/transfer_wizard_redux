from datetime import datetime
import os
import pathlib
import re


class DirectoryGenerator:

    def target_path(self, source_filepath, target_directory, filename):
        decimal_birthtime = os.stat(source_filepath).st_birthtime
        birthtime = datetime.fromtimestamp(decimal_birthtime)
        quarter = self.determine_quarter(birthtime.month)
        prospective_path = f'{target_directory}{birthtime.year}/{quarter}/{filename}'
        return self.detect_duplicates(source_filepath, prospective_path)

    def detect_duplicates(self, source_filepath, target_filepath):
        if not self.path_in_use(target_filepath):
            self.create_directory(target_filepath)
            return target_filepath
        if self.files_are_same_size(source_filepath, target_filepath):
            return ''
        else:
            return self.generate_next_available_path(source_filepath, target_filepath)

    def create_directory(self, target_filepath):  # TODO make private. how to set interface?
        path = pathlib.Path(target_filepath)
        os.makedirs(path.parent)

    def generate_next_available_path(self, source_filepath, target_filepath):
        path = pathlib.Path(target_filepath)
        filename = self.add_suffix(path.stem)
        incremented_path = f'{path.parent}/{filename}{path.suffix}'
        if self.path_in_use(incremented_path):
            return self.detect_duplicates(source_filepath, incremented_path)
        else:
            return incremented_path

    def add_suffix(self, filename):
        if bool(re.search("___", filename)):
            return self.increment_suffix_number(filename)
        else:
            return filename + '___1'

    def increment_suffix_number(self, filename):
        filename, existing_number_suffix = filename.rsplit('___', 1)
        number_suffix = str(int(existing_number_suffix) + 1)
        return filename.rsplit('___', 1)[0] + '___' + number_suffix

    def path_in_use(self, path):
        return os.path.isfile(path)

    def files_are_same_size(self, path_1, path_2):
        return os.stat(path_1).st_size == os.stat(path_2).st_size

    def determine_quarter(self, month):
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
