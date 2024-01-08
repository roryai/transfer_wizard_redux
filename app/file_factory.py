from pathlib import Path as p

from app.file import File
from app.filepath_generator import FilepathGenerator


class FileFactory:

    def __init__(self, source_filepath, destination_directory):
        self.source_filepath = source_filepath
        self.destination_directory = destination_directory

    def save_pre_copy_file_record(self):
        destination_filepath = FilepathGenerator(
            self.source_filepath, self.destination_directory).generate_destination_filepath()
        size = p(self.source_filepath).stat().st_size
        name_clash = self.__name_clash(self.source_filepath, destination_filepath)
        File(source_filepath=self.source_filepath,
             destination_filepath=destination_filepath,
             size=size,
             name_clash=name_clash
             ).save()

    def __name_clash(self, source_filepath, destination_filepath):
        if destination_filepath is None:
            return False
        source_filename = p(source_filepath).name
        destination_filename = p(destination_filepath).name
        return source_filename != destination_filename
