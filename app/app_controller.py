import os

from app.directory_manager import DirectoryManager
from app.file import File
from app.file_gateway import FileGateway
from app.filepath_generator import FilepathGenerator
from app.scanner import Scanner
from app.transfer import Transfer


class AppController:

    def __init__(self, source_directory, target_directory):
        self.source_directory = source_directory
        self.target_directory = target_directory
        self.directory_manager = DirectoryManager()

    def run(self):
        self.directory_manager.check_if_directory_exists(self.source_directory)
        self.directory_manager.create_directory_if_not_exists(self.target_directory)
        FileGateway().wipe_database()  # TODO dev only, remove later
        self.__create_db_entries_for_files_to_be_transferred()
        self.__present_stats_to_user()
        self.__user_confirmation_of_transfer()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def __create_db_entries_for_files_to_be_transferred(self):
        source_filepaths = Scanner().scan_dirs(self.source_directory)
        for source_filepath in source_filepaths:
            target_filepath = FilepathGenerator(
                source_filepath, self.target_directory).generate_target_filepath()
            size = os.stat(source_filepath).st_size
            File(source_filepath, target_filepath, size).save()

    def __present_stats_to_user(self):
        file_gateway = FileGateway()
        sum_size = file_gateway.sum_size()
        count = file_gateway.count()
        print(f'{count} files ready to be transferred.')
        print(f'Total file size: {round(sum_size / (1024 ** 2), 3)}MB')
        print(f'Source directory: {self.source_directory}')
        print(f'Target directory: {self.target_directory}')
        print()
        print(f'Proceed with transfer? ( y / n )')

    def __user_confirmation_of_transfer(self):
        if input() == 'y':
            records = FileGateway().select_all()
            for record in records:
                file = File.init_from_record(record)
                Transfer().copy_files(file.source_filepath, file.target_filepath)
