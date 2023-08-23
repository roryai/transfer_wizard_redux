import os

from app.file import File
from app.file_gateway import FileGateway
from app.filepath_generator import FilepathGenerator
from app.scanner import Scanner
from app.transfer import Transfer


class AppController:

    def run(self, source_directory, target_directory):
        for path in [source_directory, target_directory]:
            if not os.path.isdir(path):
                raise FileNotFoundError(f'{path} is not a valid directory.')

        source_directory = self.__sanitise_filepath(source_directory)
        target_directory = self.__sanitise_filepath(target_directory)

        FileGateway().wipe_database()  # TODO dev only, remove later

        # collect filepaths from source directory
        source_filepaths = Scanner().scan_dirs(source_directory)

        # generate target path, create db record including paths and size data
        for source_filepath in source_filepaths:
            target_filepath = FilepathGenerator(
                source_filepath, target_directory).generate_target_filepath()
            size = os.stat(source_filepath).st_size
            File(source_filepath, target_filepath, size).save()

        file_gateway = FileGateway()
        sum_size = file_gateway.sum_size()
        count = file_gateway.count()

        print(f'{count} files ready to be transferred.')
        print(f'Total file size: {round(sum_size / (1024 ** 2), 3)}MB')
        print(f'Source directory: {source_directory}')
        print(f'Target directory: {target_directory}')
        print()
        print(f'Proceed with transfer? ( y / n )')

        key = input()
        if key == 'y':
            # copy all files in db to target paths
            records = FileGateway().select_all()
            for record in records:
                file = File.init_from_record(record)
                Transfer().copy_files(file.source_filepath, file.target_filepath)

        FileGateway().wipe_database()  # TODO dev only, remove later

    def __sanitise_filepath(self, filepath):
        if filepath[-1] != '/':
            filepath += '/'
        return filepath
