from app.file_gateway import FileGateway


class File:

    def __init__(self, source_filepath, target_filepath, size, gateway=FileGateway):
        self.source_filepath = source_filepath
        self.target_filepath = target_filepath
        self.size = size
        self.gateway = gateway

    def insert_into_db(self):
        self.gateway().insert(self)

    @classmethod
    def init_from_record(cls, record):
        return File(record[1], record[2], record[3])

    def __eq__(self, other):
        return (
            self.source_filepath == other.source_filepath and
            self.target_filepath == other.target_filepath and
            self.size == other.size
        )
