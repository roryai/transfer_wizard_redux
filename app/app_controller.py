from app.directory_manager import DirectoryManager
from app.file import File
from app.file_builder import FileBuilder
from app.file_gateway import FileGateway
from app.scanner import Scanner
from app.transfer import Transfer


class AppController:

    def __init__(self, source_directory, target_directory):
        self.source_directory = source_directory
        self.target_directory = target_directory
        self.directory_manager = DirectoryManager()

    def run(self):
        self.directory_manager.check_if_directory_exists(self.source_directory)
        FileGateway().wipe_database()  # TODO dev only, remove later
        self.__create_db_entries_for_files_to_be_transferred()
        self.__present_stats_to_user()
        self.__user_confirmation_of_transfer()
        FileGateway().wipe_database()  # TODO dev only, remove later

    def __create_db_entries_for_files_to_be_transferred(self):
        source_filepaths = Scanner().scan_dirs(self.source_directory)
        for source_filepath in source_filepaths:
            FileBuilder(source_filepath, self.target_directory).build()

    def __present_stats_to_user(self):
        file_gateway = FileGateway()
        sum_size = file_gateway.sum_size()
        count = file_gateway.count()
        duplicates = file_gateway.duplicate_count()
        name_clashes = file_gateway.name_clashes_count()
        print()
        print(f'{count} files selected to be transferred.')
        print(f'Total file size: {round(sum_size / (1024 ** 2), 3)}MB')
        print(f'{duplicates} files are duplicates. Duplicates will not be copied')
        print(f'{name_clashes} files had name clashes. Files will be copied with a suffix.')
        print(f'Source directory: {self.source_directory}')
        print(f'Target directory: {self.target_directory}')
        print()
        print(f'Proceed with transfer? ( y / n )')
        print()

    def __user_confirmation_of_transfer(self):
        if input() == 'y':
            records = FileGateway().select_all()
            for record in records:
                file = File.init_from_record(record)
                Transfer().copy_files(file.source_filepath, file.target_filepath)
