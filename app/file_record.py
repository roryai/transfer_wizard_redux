from app.file_gateway import FileGateway


class FileRecord:

    def insert(self, file):
        FileGateway().insert(file)

    def map_from_record(self, record):
        return {
            'source_filepath': record[1],
            'target_filepath': record[2],
            'size': record[3],
            'copied': record[4],
            'name_clash': record[5]
        }
