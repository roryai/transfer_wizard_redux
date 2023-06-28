import pathlib
import shutil

from app.directory_generator import DirectoryGenerator


class Transfer:

    def copy_files(self, source_files, target_directory):
        for source_filepath in source_files:
            filename = pathlib.Path(source_filepath).name
            target_filepath = DirectoryGenerator().target_path(
                source_filepath, target_directory, filename)
            if target_filepath:
                shutil.copy2(source_filepath, target_filepath)
