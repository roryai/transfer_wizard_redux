import os
import pathlib
import shutil
import re


class Transfer:

    def copy_files(self, source_files, target_directory):
        for source_filepath in source_files:
            prospective_target_filepath = target_directory + pathlib.Path(source_filepath).name
            target_filepath = self.handle_duplicates(source_filepath, prospective_target_filepath)
            if target_filepath:
                shutil.copy2(source_filepath, target_filepath)

    def handle_duplicates(self, source_filepath, target_filepath):
        if not self.path_in_use(target_filepath):
            return target_filepath
        if self.files_are_same_size(source_filepath, target_filepath):
            return ''
        else:
            return self.generate_next_available_path(source_filepath, target_filepath)

    def generate_next_available_path(self, source_filepath, target_filepath):
        path = pathlib.Path(target_filepath)
        filename = self.add_suffix(path.stem)
        incremented_path = f'{path.parent}/{filename}{path.suffix}'
        if self.path_in_use(incremented_path):
            return self.handle_duplicates(source_filepath, incremented_path)
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
