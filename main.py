import argparse

from app.app_controller import AppController
from app.db_initializer import DBInitializer
from app.directory_manager import DirectoryManager
from app.extension_scanner import ExtensionScanner
from app.logger import Logger

if __name__ == '__main__':
    program_description = """This program copies media files to an organised directory structure.
        Example usage:
        python main.py -s path/to/source -d path/to/destination  <-- To copy files from source to destination.
        python main.py -s path/to/source -ext  <-- To discover miscellaneous extensions."""

    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-s', '--source', type=str, required=True, help='Source directory path.')
    parser.add_argument('-d', '--destination', type=str, required=False, help='Destination directory path.')
    parser.add_argument('-ext', '--extensions', action='store_true', default=False, required=False,
                        help='Displays miscellaneous extensions in source directory.')
    args = parser.parse_args()

    DBInitializer().init_prod_database()

    if args.extensions:
        DirectoryManager().check_if_directory_exists(args.source)
        ExtensionScanner(args.source).display_misc_extensions()
    elif args.destination:
        DirectoryManager().check_if_directory_exists(args.source)
        DirectoryManager().check_if_directory_exists(args.destination)
        Logger().init_log_file(args.destination)
        AppController(destination_root_directory=args.destination,
                      source_directory=args.source).copy_files_from_source_to_destination()
    else:
        error_message = "Must provide source flag (-s <directory path>) and either -ext flag or " \
                        "-d flag (-d <directory path>"
        raise argparse.ArgumentError(None, error_message)
