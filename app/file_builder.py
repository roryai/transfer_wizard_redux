from pathlib import Path as p

from app.file import File
from app.filepath_generator import FilepathGenerator


class FileBuilder:

    def __init__(self, source_filepath, target_directory):
        self.source_filepath = source_filepath
        self.target_directory = target_directory

    def build(self):
        target_filepath = FilepathGenerator(
            self.source_filepath, self.target_directory).generate_target_filepath()
        size = p(self.source_filepath).stat().st_size
        name_clash = self.__name_clash(self.source_filepath, target_filepath)
        File(source_filepath=self.source_filepath,
             target_filepath=target_filepath,
             size=size,
             name_clash=name_clash
             ).save()

    def __name_clash(self, source_filepath, target_filepath):
        source_filename = p(source_filepath).name
        target_filename = p(target_filepath).name
        return source_filename != target_filename
