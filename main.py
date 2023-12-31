import argparse

from app.app_controller import AppController
from app.db_initializer import DBInitializer
from app.extension_scanner import ExtensionScanner

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""This program copies media files to an organised directory structure.
Example usage:
python main.py -s path/to/source -d path/to/destination  <-- To copy files from source to destination.
python main.py -s path/to/source -ext  <-- To discover invalid extensions.""")

    parser.add_argument('-s', '--source', type=str, required=True, help='Source directory path.')
    parser.add_argument('-d', '--destination', type=str, required=False, help='Destination directory path.')
    parser.add_argument('-ext', '--extensions', action='store_true', default=False, required=False,
                        help='Displays invalid extensions in source directory.')

    args = parser.parse_args()

    DBInitializer().init_prod_database()

    if args.extensions:
        ExtensionScanner(args.source).display_invalid_extensions()
    elif args.destination:
        AppController(args.source).copy_files_from_source_to(args.destination)
    else:
        error_message = "Must provide source flag (-s <directory path>) and either -ext flag or " \
                        "-d flag (-d <directory path>"
        raise argparse.ArgumentError(None, error_message)
