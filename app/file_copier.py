from pathlib import Path
import shutil

from app.directory_manager import DirectoryManager
from app.file import File
from app.file_gateway import FileGateway
from app.logger import Logger


class FileCopier:

    def __init__(self, directory_manager=DirectoryManager, file_gateway=FileGateway):
        self.directory_manager = directory_manager()
        self.file_gateway = file_gateway()

    def copy_source_files_to_destination(self):
        while candidate_file_record := self.file_gateway.select_one_where_copy_not_attempted():
            self._prepare_destination_and_attempt_copy(candidate_file_record)

    def _prepare_destination_and_attempt_copy(self, candidate_file_record):
        file = File.init_from_record(candidate_file_record)
        self.directory_manager.create_directory_if_not_exists(file.destination_directory())
        self._copy_file(file)
        return self.file_gateway.select_one_where_copy_not_attempted()

    def _copy_file(self, file):
        shutil.copy2(file.source_filepath, file.destination_filepath)
        self._copy_success(file) if self._confirm_file_copy(file) else self._copy_failure(file)
        self.file_gateway.update_copied(file.copied, file.copy_attempted, file.source_filepath)

    def _confirm_file_copy(self, file):
        return Path(file.destination_filepath).is_file()

    def _copy_success(self, file):
        file.copied = True
        file.copy_attempted = True
        Logger().log_successful_copy(file.source_filepath, file.destination_filepath)

    def _copy_failure(self, file):
        file.copied = False
        file.copy_attempted = True
        Logger().log_unsuccessful_copy(file.source_filepath, file.destination_filepath)
