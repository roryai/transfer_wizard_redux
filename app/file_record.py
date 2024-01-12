from app.file_gateway import FileGateway


class FileRecord:

    def insert(self, file):
        FileGateway().insert(file)

    def map_from_record(self, record):
        return {
            'source_filepath': record[1],
            'destination_filepath': record[2],
            'size': record[3],
            'copied': self.__convert_boolean(record[4]),
            'name_clash': self.__convert_boolean(record[5]),
            'media': self.__convert_boolean(record[6]),
            'copy_attempted': self.__convert_boolean(record[7])
        }

    def __convert_boolean(self, val):
        return val == 1
