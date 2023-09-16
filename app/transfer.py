from pathlib import Path as p
import shutil

from app.directory_manager import DirectoryManager


class Transfer:

    def copy_files(self, source_filepath, target_filepath,
                   directory_manager=DirectoryManager):
        target_directory = p(target_filepath).parent
        directory_manager().create_directory_if_not_exists(target_directory)
        if target_filepath:
            shutil.copy2(source_filepath, target_filepath)
