import datetime
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
        Logger().init_log_file(destination_root_directory)

    def copy_files(self):
        start = datetime.datetime.now()
        self._prepare_database_records()
        stats = StatPresenter(self.source_root_directory,
                              self.destination_root_directory).print_stats_summary()
        end = datetime.datetime.now()
        print(f'Time taken to scan source directory: {end - start}')
        self._perform_copy(stats) if self._user_confirms_copy() else None

    def _prepare_database_records(self):
        FileGateway().wipe_database()  # TODO dev only, remove later
        self._create_db_records_for_files_to_be_copied()

    def _create_db_records_for_files_to_be_copied(self):
        file_paths = self._scan_files_in_source_directory()
        [FileFactory(source_filepath=src,
                     destination_root_directory=self.destination_root_directory
                     ).save_pre_copy_file_record(media=media)
         for src, media in file_paths]

    def _scan_files_in_source_directory(self):
        return itertools.chain(
            ((src, True) for src in self._media_source_filepaths()),
            ((src, False) for src in self._misc_source_filepaths()))

    def _media_source_filepaths(self):
        return Scanner().media_filepaths_in(self.source_root_directory)

    def _misc_source_filepaths(self):
        return Scanner().misc_filepaths_in(
            self.source_root_directory) if self.include_misc_files else []

    def _perform_copy(self, stats):
        Logger().log_to_file(stats)
        FileCopier().copy_source_files_to_destination()
        self._post_copy_logging_and_display()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def _user_confirms_copy(self):
        print(f'\nProceed with copy? ( y / n )')
        return input().lower() == 'y'

    def _post_copy_logging_and_display(self):
        Logger().append_summary_to_file()
        error_messages = Logger().append_errors_to_logfile()
        print(error_messages) if error_messages else None
