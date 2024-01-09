from app.directory_manager import DirectoryManager
from app.file_factory import FileFactory
from app.file_gateway import FileGateway
from app.scanner import Scanner
from app.stat_presenter import StatPresenter
from app.file_copier import FileCopier
from app.logger import Logger


class AppController:

    def __init__(self, destination_directory, source_directory):
        DirectoryManager().check_if_directory_exists(source_directory)
        self.source_directory = source_directory
        self.destination_directory = destination_directory

    def copy_files_from_source_to_destination(self):
        FileGateway().wipe_database()  # TODO dev only, remove later
        self.__create_db_records_for_files_to_be_copied(self.destination_directory)
        StatPresenter().present_analysis_of_candidate_files(self.source_directory, self.destination_directory)
        if self.__user_confirmation_of_copy():
            FileCopier().copy_source_files_to_destination()
        self.__display_errors()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def __create_db_records_for_files_to_be_copied(self, destination_directory):
        source_filepaths = Scanner().valid_filepaths_in(self.source_directory)
        for source_filepath in source_filepaths:
            FileFactory(source_filepath, destination_directory).save_pre_copy_file_record()

    def __user_confirmation_of_copy(self):
        print()
        print(f'Proceed with copy? ( y / n )')
        if input() == 'y':
            return True

    def __display_errors(self):
        error_messages = Logger().write_errors_to_logfile()
        print(error_messages) if error_messages else None
