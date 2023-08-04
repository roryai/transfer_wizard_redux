from pathlib import Path
import shutil

from app.directory_creator import DirectoryCreator


class Transfer:

    def copy_files(self, source_filepath, target_filepath,
                   directory_creator=DirectoryCreator):
        target_directory = Path(target_filepath).parent
        directory_creator(target_directory).create_directory()  # perform a check to see if required?
        if target_filepath:
            shutil.copy2(source_filepath, target_filepath)
