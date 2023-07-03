from pathlib import Path


class DirectoryCreator:

    def create_directory(self, target_directory):
        Path(target_directory).mkdir(parents=True, exist_ok=True)
