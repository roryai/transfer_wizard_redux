from pathlib import Path
import shutil

from app.filepath_generator import FilepathGenerator
from app.directory_creator import DirectoryCreator


class Transfer:

    def copy_files(self, source_files, target_directory):
        for source_filepath in source_files:
            filename = Path(source_filepath).name
            target_filepath = FilepathGenerator().generate_target_filepath(
                source_filepath, target_directory, filename)
            target_directory = Path(target_filepath).parent
            DirectoryCreator().create_directory(target_directory)
            if target_filepath:
                shutil.copy2(source_filepath, target_filepath)
