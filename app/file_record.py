from app.file_gateway import FileGateway


class FileRecord:

    def insert(self, file):
        FileGateway().insert(file)

    def map_from_record(self, record):
        return {
            'source_filepath': record[1],
            'destination_filepath': record[2],
            'size': record[3],
            'copied': bool(record[4]),
            'name_clash': bool(record[5]),
            'media': bool(record[6]),
            'copy_attempted': bool(record[7])
        }
