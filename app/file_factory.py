from pathlib import Path

from app.file import File
from app.filepath_generator import FilepathGenerator


class FileFactory:

    def __init__(self, source_filepath, destination_root_directory):
        self.source_filepath = source_filepath
        self.destination_root_directory = destination_root_directory

    def save_pre_copy_file_record(self, media, et):
        destination_filepath = FilepathGenerator(
            source_filepath=self.source_filepath,
            destination_root_directory=self.destination_root_directory
        ).generate_destination_filepath(media, et)
        size = Path(self.source_filepath).stat().st_size
        name_clash = self._name_clash(self.source_filepath, destination_filepath)
        File(source_filepath=self.source_filepath, destination_filepath=destination_filepath,
             size=size, name_clash=name_clash, copied=False, media=media, copy_attempted=False
             ).save()

    def _name_clash(self, source_filepath, destination_filepath):
        if destination_filepath is None:
            return False
        # names will be different if destination filename has incremented suffix
        return Path(source_filepath).name != Path(destination_filepath).name
