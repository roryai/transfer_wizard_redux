from app.file_factory import FileFactory
from app.file_gateway import FileGateway
from app.scanner import Scanner
from app.stat_presenter import StatPresenter
from app.file_copier import FileCopier
from app.logger import Logger


class AppController:

    def __init__(self, destination_root_directory, source_root_directory):
        self.source_root_directory = source_root_directory
        self.destination_root_directory = destination_root_directory
        self.stat_presenter = StatPresenter(source_root_directory, destination_root_directory)

    def copy_files_from_source_to_destination(self):
        FileGateway().wipe_database()  # TODO dev only, remove later
        self.__create_db_records_for_files_to_be_copied(self.destination_root_directory)
        self.stat_presenter.print_stats_summary()
        if self.__user_confirms_copy():
            Logger().init_log_file(self.destination_root_directory)
            self.stat_presenter.log_pre_copy_stats()
            FileCopier().copy_source_files_to_destination()
            self.__display_errors()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def __create_db_records_for_files_to_be_copied(self, destination_root_directory):
        source_filepaths = Scanner().media_filepaths_in(self.source_root_directory)
        for source_filepath in source_filepaths:
            FileFactory(source_filepath, destination_root_directory).save_pre_copy_file_record()

    def __user_confirms_copy(self):
        print(f'\nProceed with copy? ( y / n )')
        if input() == 'y':
            return True

    def __display_errors(self):
        error_messages = Logger().write_errors_to_logfile()
        print(error_messages) if error_messages else None
