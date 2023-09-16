from pathlib import Path as p


class DirectoryManager:

    def create_directory_if_not_exists(self, target_directory):
        p(target_directory).mkdir(parents=True, exist_ok=True)

    def check_if_directory_exists(self, directory_path):
        if not p(directory_path).is_dir():
            raise FileNotFoundError(f'{directory_path} is not a valid directory.')
