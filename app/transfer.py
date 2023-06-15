import os
import pathlib
import shutil
import re


class Transfer:

    def copy_files(self, source_files, target_directory):
        for filepath in source_files:
            filename = pathlib.Path(filepath).name
            target_path = target_directory + filename
            if os.path.isfile(target_path):
                if os.stat(filepath).st_size == os.stat(target_path).st_size:
                    continue
                else:
                    target_path = self.add_number_suffix(target_path)
            shutil.copy2(filepath, target_path)

    def add_number_suffix(self, filepath):
        path = pathlib.Path(filepath)
        target_dir = path.parent
        file_stem = path.stem
        file_ext = path.suffix
        if bool(re.search("___", file_stem)):
            file_stem, existing_number_suffix = file_stem.rsplit('___', 1)
            number_suffix = str(int(existing_number_suffix) + 1)
        else:
            number_suffix = '1'
        return f'{target_dir}/{file_stem}___{number_suffix}{file_ext}'
