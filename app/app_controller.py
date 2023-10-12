from app.directory_manager import DirectoryManager
from app.file_factory import FileFactory
from app.file_gateway import FileGateway
from app.scanner import Scanner
from app.stat_presenter import StatPresenter
from app.file_copier import FileCopier


class AppController:

    def __init__(self, source_directory, target_directory):
        self.source_directory = source_directory
        self.target_directory = target_directory

    def run(self):
        DirectoryManager().check_if_directory_exists(self.source_directory)
        FileGateway().wipe_database()  # TODO dev only, remove later
        self.__create_db_records_for_files_to_be_copied()
        StatPresenter().present_analysis_of_candidate_files(self.source_directory, self.target_directory)
        self.__user_confirmation_of_copy()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def __create_db_records_for_files_to_be_copied(self):
        source_filepaths = Scanner().scan_directory(self.source_directory)
        for source_filepath in source_filepaths:
            FileFactory(source_filepath, self.target_directory).create_pre_copy_file()

    def __user_confirmation_of_copy(self):
        print()
        print(f'Proceed with copy? ( y / n )')
        if input() == 'y':
            FileCopier().copy_source_files_to_target_directory()
