from app.file_record import FileRecord


class File:

    def __init__(self, source_filepath, target_filepath, size, copied=None, name_clash=False):
        self.source_filepath = source_filepath
        self.target_filepath = target_filepath
        self.size = size
        self.copied = copied
        self.name_clash = name_clash

    def __eq__(self, other):
        return (
                self.source_filepath == other.source_filepath and
                self.target_filepath == other.target_filepath and
                self.size == other.size and
                self.copied == other.copied and
                self.name_clash == other.name_clash
        )

    def save(self):
        FileRecord().insert(self)

    @classmethod
    def init_from_record(cls, record):
        vals = FileRecord().map_from_record(record)
        return File(
            source_filepath=vals['source_filepath'],
            target_filepath=vals['target_filepath'],
            size=vals['size'],
            copied=cls.__set_copied(vals['copied']),
            name_clash=True if vals['name_clash'] == 1 else False
        )

    @classmethod
    def __set_copied(cls, record_val):
        if record_val is None:
            return None
        return True if record_val == 1 else False
