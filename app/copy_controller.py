from app.file_factory import FileFactory
from app.file_gateway import FileGateway
from app.scanner import Scanner
from app.stat_presenter import StatPresenter
from app.file_copier import FileCopier
from app.logger import Logger


class CopyController:

    def __init__(self, destination_root_directory, source_root_directory):
        self.source_root_directory = source_root_directory
        self.destination_root_directory = destination_root_directory

    def copy_media_files(self):
        self.__prepare_database_records()
        stats = StatPresenter(self.source_root_directory,
                              self.destination_root_directory).print_stats_summary()
        self.__perform_copy(stats) if self.__user_confirms_copy() else None

    def __prepare_database_records(self):
        FileGateway().wipe_database()  # TODO dev only, remove later
        self.__create_db_records_for_files_to_be_copied()

    def __create_db_records_for_files_to_be_copied(self):
        source_filepaths = Scanner().media_filepaths_in(self.source_root_directory)
        [FileFactory(src, self.destination_root_directory).save_pre_copy_file_record()
         for src in source_filepaths]

    def __user_confirms_copy(self):
        print(f'\nProceed with copy? ( y / n )')
        return input().lower() == 'y'

    def __perform_copy(self, stats):
        self.__pre_copy_logging(stats)
        FileCopier().copy_source_files_to_destination()
        self.__post_copy_error_logging_and_display()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def __pre_copy_logging(self, stats):
        Logger().init_log_file(self.destination_root_directory)
        Logger().log_to_file(stats)

    def __post_copy_error_logging_and_display(self):
        error_messages = Logger().append_errors_to_logfile()
        print(error_messages) if error_messages else None
