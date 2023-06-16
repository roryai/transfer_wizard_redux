import os
import pathlib
import shutil
import re


class Transfer:

    def copy_files(self, source_files, target_directory):
        for source_filepath in source_files:
            target_path = target_directory + pathlib.Path(source_filepath).name
            if self.file_already_exists(target_path):
                if self.files_are_same_size(source_filepath, target_path):
                    continue
                else:
                    target_path = self.generate_next_available_path(target_path)
            shutil.copy2(source_filepath, target_path)

    def generate_next_available_path(self, target_path):
        path = pathlib.Path(target_path)
        target_dir = path.parent
        file_stem = path.stem
        file_ext = path.suffix

        file_stem = self.add_suffix(file_stem)
        next_increment_path = self.construct_path(target_dir, file_stem, file_ext)
        if self.file_already_exists(next_increment_path):
            # TODO if same size, abandon this iteration
            return self.generate_next_available_path(next_increment_path)
        else:
            return self.construct_path(target_dir, file_stem, file_ext)

    def add_suffix(self, file_stem):
        if bool(re.search("___", file_stem)):
            return self.increment_number_suffix(file_stem)
        else:
            return file_stem + '___1'

    def construct_path(self, target_dir, file_stem, file_ext):
        return f'{target_dir}/{file_stem}{file_ext}'

    def increment_number_suffix(self, file_stem):
        file_stem, existing_number_suffix = file_stem.rsplit('___', 1)
        number_suffix = str(int(existing_number_suffix) + 1)
        return file_stem.rsplit('___', 1)[0] + '___' + number_suffix

    def file_already_exists(self, path):
        return os.path.isfile(path)

    def files_are_same_size(self, path_1, path_2):
        return os.stat(path_1).st_size == os.stat(path_2).st_size