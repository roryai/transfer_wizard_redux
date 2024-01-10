from pathlib import Path

from app.file_record import FileRecord


class File:

    def __init__(self, source_filepath, destination_filepath, size,
                 copied=None, name_clash=False, media=True):
        self.source_filepath = source_filepath
        self.destination_filepath = destination_filepath
        self.size = size
        self.copied = copied
        self.name_clash = name_clash
        self.media = media

    def __eq__(self, other):
        return (
                self.source_filepath == other.source_filepath and
                self.destination_filepath == other.destination_filepath and
                self.size == other.size and
                self.copied == other.copied and
                self.name_clash == other.name_clash and
                self.media == other.media
        )

    def save(self):
        FileRecord().insert(self)

    def destination_directory(self):
        return Path(self.destination_filepath).parent

    @classmethod
    def init_from_record(cls, record):
        vals = FileRecord().map_from_record(record)
        return File(
            source_filepath=vals['source_filepath'],
            destination_filepath=vals['destination_filepath'],
            size=vals['size'],
            copied=cls.__set_copied(vals['copied']),
            name_clash=True if vals['name_clash'] == 1 else False,
            media=vals['media']
        )

    @classmethod
    def __set_copied(cls, record_val):
        if record_val is None:
            return None
        return True if record_val == 1 else False
