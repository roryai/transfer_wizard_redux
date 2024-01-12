from pathlib import Path

from app.file import File
from app.filepath_generator import FilepathGenerator


class FileFactory:

    def __init__(self, source_filepath, destination_root_directory):
        self.source_filepath = source_filepath
        self.destination_root_directory = destination_root_directory

    def save_pre_copy_file_record(self, media=True):  # TODO remove default val when adding misc file functionality
        destination_filepath = FilepathGenerator(
            self.source_filepath, self.destination_root_directory).generate_destination_filepath()
        size = Path(self.source_filepath).stat().st_size
        name_clash = self.__name_clash(self.source_filepath, destination_filepath)
        File(source_filepath=self.source_filepath,
             destination_filepath=destination_filepath,
             size=size,
             name_clash=name_clash,
             copied=None,  # TODO set to false after making column not null
             media=media,
             copy_attempted=False).save()

    def __name_clash(self, source_filepath, destination_filepath):
        if destination_filepath is None:
            return False
        source_filename = Path(source_filepath).name
        destination_filename = Path(destination_filepath).name
        return source_filename != destination_filename
