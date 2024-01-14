import argparse
import pathlib
import sys

from app.copy_controller import CopyController
from app.db_initializer import DBInitializer
from app.directory_manager import DirectoryManager
from app.extension_presenter import ExtensionPresenter

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
program_description = """
This program copies media files to an organised directory structure.
Example usage:
python main.py -s path/to/source -d path/to/destination  <-- To copy files from source to destination || 
python main.py -s path/to/directory -ext  <-- To discover miscellaneous file extensions in directory."""


def main():
    DBInitializer(ROOT_DIR).init_prod_database()
    args = configure_parser().parse_args(sys.argv[1:])
    if args.extensions:
        DirectoryManager().check_if_directory_exists(args.source)
        ExtensionPresenter(args.source).display_misc_extensions()
    elif args.destination:
        DirectoryManager().check_if_directory_exists(args.source)
        DirectoryManager().check_if_directory_exists(args.destination)
        CopyController(destination_root_directory=args.destination,
                       source_root_directory=args.source).copy_media_files()
    else:
        error_message = "Must provide source flag (-s <directory path>) and either -ext flag or " \
                        "-d flag (-d <directory path>)"
        raise argparse.ArgumentError(None, error_message)


def configure_parser():
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-s', '--source', type=str, required=True, help='Source directory path.')
    parser.add_argument('-d', '--destination', type=str, required=False, help='Destination directory path.')
    parser.add_argument('-ext', '--extensions', action='store_true', default=False, required=False,
                        help='Displays miscellaneous extensions in source directory.')
    return parser


if __name__ == '__main__':
    main()
