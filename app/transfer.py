import os
import pathlib
import shutil


class Transfer:

    def copy_files(self, source_files, target_directory):
        for file in source_files:
            filename = pathlib.Path(file).name
            target_path = target_directory + filename
            if os.path.isfile(target_path):
                continue
            shutil.copy2(file, target_path)
