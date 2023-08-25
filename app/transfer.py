from pathlib import Path
import shutil

from app.directory_manager import DirectoryManager


class Transfer:

    def copy_files(self, source_filepath, target_filepath,
                   directory_creator=DirectoryManager):
        target_directory = Path(target_filepath).parent
        directory_creator().create_directory_if_not_exists(target_directory)  # perform a check to see if required?
        if target_filepath:
            shutil.copy2(source_filepath, target_filepath)
