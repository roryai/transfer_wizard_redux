from pathlib import Path as p
import shutil

from app.directory_manager import DirectoryManager
from app.file import File
from app.file_gateway import FileGateway


class FileCopier:

    def __init__(self, logger, directory_manager=DirectoryManager, file_gateway=FileGateway):
        self.directory_manager = directory_manager()
        self.file_gateway = file_gateway()
        self.logger = logger

    def copy_source_files_to_destination(self):
        record = self.file_gateway.select_one_file_where_copy_not_attempted()
        while record:
            file = File.init_from_record(record)
            self.directory_manager.create_directory_if_not_exists(file.destination_directory())
            self.__copy_file(file)
            record = self.file_gateway.select_one_file_where_copy_not_attempted()

    def __copy_file(self, file):
        shutil.copy2(file.source_filepath, file.destination_filepath)
        if self.__file_copied(file):
            file.copied = True
            self.logger.log_successful_copy(file.source_filepath, file.destination_filepath)
        else:
            file.copied = False
            self.logger.log_unsuccessful_copy(file.source_filepath, file.destination_filepath)
        self.file_gateway.update_copied(file)

    def __file_copied(self, file):
        return p(file.destination_filepath).is_file()
