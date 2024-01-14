import itertools

from app.file_factory import FileFactory
from app.file_gateway import FileGateway
from app.scanner import Scanner
from app.stat_presenter import StatPresenter
from app.file_copier import FileCopier
from app.logger import Logger


class CopyController:

    def __init__(self, destination_root_directory, source_root_directory, include_misc_files):
        self.source_root_directory = source_root_directory
        self.destination_root_directory = destination_root_directory
        self.include_misc_files = include_misc_files

    def copy_files(self):
        self.__prepare_database_records()
        stats = StatPresenter(self.source_root_directory,
                              self.destination_root_directory).print_stats_summary()
        self.__perform_copy(stats) if self.__user_confirms_copy() else None

    def __prepare_database_records(self):
        FileGateway().wipe_database()  # TODO dev only, remove later
        self.__create_db_records_for_files_to_be_copied()

    def __create_db_records_for_files_to_be_copied(self):
        file_paths = self.__scan_files_in_source_directory()
        [FileFactory(src, self.destination_root_directory).save_pre_copy_file_record(media=media)
         for src, media in file_paths]

    def __scan_files_in_source_directory(self):
        return itertools.chain(
            ((src, True) for src in self.__media_source_filepaths()),
            ((src, False) for src in self.__misc_source_filepaths()))

    def __media_source_filepaths(self):
        return Scanner().media_filepaths_in(self.source_root_directory)

    def __misc_source_filepaths(self):
        return Scanner().misc_filepaths_in(
            self.source_root_directory) if self.include_misc_files else []

    def __perform_copy(self, stats):
        self.__pre_copy_logging(stats)
        FileCopier().copy_source_files_to_destination()
        self.__post_copy_error_logging_and_display()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def __user_confirms_copy(self):
        print(f'\nProceed with copy? ( y / n )')
        return input().lower() == 'y'

    def __pre_copy_logging(self, stats):
        Logger().init_log_file(self.destination_root_directory)
        Logger().log_to_file(stats)

    def __post_copy_error_logging_and_display(self):
        error_messages = Logger().append_errors_to_logfile()
        print(error_messages) if error_messages else None
