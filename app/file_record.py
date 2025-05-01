from pathlib import Path

from app.file_gateway import FileGateway


class FileRecord:

    def insert(self, file):
        FileGateway().insert(file)

    def map_from_record(self, record):
        return {
            'source_filepath': Path(record[1]),
            'destination_filepath': Path(record[2]) if record[2] is not None else None,
            'size': record[3],
            'copied': bool(record[4]),
            'name_clash': bool(record[5]),
            'copy_attempted': bool(record[6])
        }
