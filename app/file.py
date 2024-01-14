from pathlib import Path

from app.file_record import FileRecord


class File:

    def __init__(self, source_filepath, destination_filepath, size,
                 copied, name_clash, media, copy_attempted):
        self.source_filepath = source_filepath
        self.destination_filepath = destination_filepath
        self.size = size
        self.copied = copied
        self.name_clash = name_clash
        self.media = media
        self.copy_attempted = copy_attempted

    def __eq__(self, other):
        return (
                self.source_filepath == other.source_filepath and
                self.destination_filepath == other.destination_filepath and
                self.size == other.size and
                self.copied is other.copied and
                self.name_clash is other.name_clash and
                self.media is other.media and
                self.copy_attempted is other.copy_attempted
        )

    def save(self):
        FileRecord().insert(self)

    def destination_directory(self):
        return Path(self.destination_filepath).parent

    @classmethod
    def init_from_record(cls, record):
        return cls(**FileRecord().map_from_record(record))
