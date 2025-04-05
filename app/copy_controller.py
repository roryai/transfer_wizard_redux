import datetime

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
        file_paths = [src for src in self._media_source_filepaths()]
        [FileFactory(source_filepath=src,
                     destination_root_directory=self.destination_root_directory
                     ).save_pre_copy_file_record()
         for src in file_paths]

    def _media_source_filepaths(self):
        return Scanner().media_filepaths_in(self.source_root_directory)

    def _perform_copy(self, stats):
        Logger().log_to_file(stats)
        FileCopier().copy_source_files_to_destination()
        Logger().finalise_logging()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def _user_confirms_copy(self):
        print(f'\nProceed with copy? ( y / n )')
        return input().lower() == 'y'
