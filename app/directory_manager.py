import os
from pathlib import Path


class DirectoryManager:

    def create_directory_if_not_exists(self, target_directory):
        Path(target_directory).mkdir(parents=True, exist_ok=True)

    def check_if_directory_exists(self, directory_path):
        if not os.path.isdir(directory_path):
            raise FileNotFoundError(f'{directory_path} is not a valid directory.')
