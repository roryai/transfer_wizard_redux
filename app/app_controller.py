from app.directory_manager import DirectoryManager
from app.file_builder import FileBuilder
from app.file_gateway import FileGateway
from app.scanner import Scanner
from app.stat_presenter import StatPresenter
from app.transfer import Transfer


class AppController:

    def __init__(self, source_directory, target_directory):
        self.source_directory = source_directory
        self.target_directory = target_directory

    def run(self):
        DirectoryManager().check_if_directory_exists(self.source_directory)
        FileGateway().wipe_database()  # TODO dev only, remove later
        self.__create_db_records_for_files_to_be_transferred()
        StatPresenter().present_stats_to_user(self.source_directory, self.target_directory)
        self.__user_confirmation_of_transfer()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def __create_db_records_for_files_to_be_transferred(self):
        source_filepaths = Scanner().scan_directory(self.source_directory)
        for source_filepath in source_filepaths:
            FileBuilder(source_filepath, self.target_directory).build()

    def __user_confirmation_of_transfer(self):
        print(f'Proceed with transfer? ( y / n )')
        if input() == 'y':
            Transfer().copy_files()
