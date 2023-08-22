from app.file_record import FileRecord


class File:

    def __init__(self, source_filepath, target_filepath, size):
        self.source_filepath = source_filepath
        self.target_filepath = target_filepath
        self.size = size

    def save(self):
        FileRecord().insert(self)

    @classmethod
    def init_from_record(cls, record):
        vals = FileRecord().map_from_record(record)
        return File(
            vals['source_filepath'],
            vals['target_filepath'],
            vals['size']
        )

    def __eq__(self, other):
        return (
                self.source_filepath == other.source_filepath and
                self.target_filepath == other.target_filepath and
                self.size == other.size
        )
