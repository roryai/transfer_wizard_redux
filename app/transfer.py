from pathlib import Path
import shutil

from app.directory_generator import DirectoryGenerator
from app.directory_creator import DirectoryCreator


class Transfer:

    def copy_files(self, source_files, target_directory):
        for source_filepath in source_files:
            filename = Path(source_filepath).name
            target_filepath = DirectoryGenerator().prepare_target_path(
                source_filepath, target_directory, filename)
            target_directory = Path(target_filepath).parent
            DirectoryCreator().create_directory(target_directory)
            if target_filepath:
                shutil.copy2(source_filepath, target_filepath)
