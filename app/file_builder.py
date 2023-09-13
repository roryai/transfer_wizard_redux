import os
from pathlib import Path

from app.file import File
from app.filepath_generator import FilepathGenerator


class FileBuilder:

    def __init__(self, source_filepath, target_directory):
        self.source_filepath = source_filepath
        self.target_directory = target_directory

    def build(self):
        target_filepath = FilepathGenerator(
            self.source_filepath, self.target_directory).generate_target_filepath()
        size = os.stat(self.source_filepath).st_size
        name_clash = self.__name_clash(self.source_filepath, target_filepath)
        File(self.source_filepath, target_filepath, size, name_clash).save()

    def __name_clash(self, source_filepath, target_filepath):
        source_filename = Path(source_filepath).name
        target_filename = Path(target_filepath).name
        return source_filename != target_filename
