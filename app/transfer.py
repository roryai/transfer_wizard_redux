from pathlib import Path as p
import shutil

from app.directory_manager import DirectoryManager
from app.file import File
from app.file_gateway import FileGateway


class Transfer:

    def __init__(self, directory_manager=DirectoryManager, file_gateway=FileGateway):
        self.directory_manager = directory_manager()
        self.file_gateway = file_gateway()

    def copy_files(self):
        record = self.file_gateway.select_one_file_where_copy_not_attempted()
        while record:
            file = File.init_from_record(record)
            target_directory = p(file.target_filepath).parent
            self.directory_manager.create_directory_if_not_exists(target_directory)
            self.__copy_file(file)
            record = self.file_gateway.select_one_file_where_copy_not_attempted()

    def __copy_file(self, file):
        shutil.copy2(file.source_filepath, file.target_filepath)
        if self.__file_copied(file):
            file.copied = True
        else:
            file.copied = False
        self.file_gateway.update_copied(file)

    def __file_copied(self, file):
        return p(file.target_filepath).is_file()
