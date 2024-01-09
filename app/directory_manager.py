from pathlib import Path


class DirectoryManager:

    def create_directory_if_not_exists(self, destination_directory):
        Path(destination_directory).mkdir(parents=True, exist_ok=True)

    def check_if_directory_exists(self, directory_path):
        if not Path(directory_path).is_dir():
            raise FileNotFoundError(f'{directory_path} is not a valid directory.')
