import pathlib
import shutil


class Transfer:

    def copy_files(self, source_files, target_directory):
        for file in source_files:
            filename = pathlib.Path(file).name
            shutil.copy2(file, target_directory + filename)
