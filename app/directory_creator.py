from pathlib import Path


class DirectoryCreator:

    def __init__(self, target_directory):
        self.target_directory = target_directory

    def create_directory(self):
        Path(self.target_directory).mkdir(parents=True, exist_ok=True)
