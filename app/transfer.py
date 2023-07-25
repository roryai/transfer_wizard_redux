from pathlib import Path
import shutil

from app.filepath_generator import FilepathGenerator
from app.directory_creator import DirectoryCreator


class Transfer:

    def copy_files(self, source_files, target_directory,
                   filepath_generator=FilepathGenerator,
                   directory_creator=DirectoryCreator):
        for source_filepath in source_files:
            target_filepath = filepath_generator(
                source_filepath, target_directory).generate_target_filepath()
            target_directory = Path(target_filepath).parent
            directory_creator(target_directory).create_directory()
            if target_filepath:
                shutil.copy2(source_filepath, target_filepath)
