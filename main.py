import argparse
import pathlib
import sys

from app.copy_controller import CopyController
from app.db_initializer import DBInitializer
from app.directory_manager import DirectoryManager
from app.extension_presenter import ExtensionPresenter

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
PROGRAM_DESCRIPTION = """
This program copies photos and videos to directory structure based on capture date:

└── destination_directory
    └── 2024
        └── Q1
            └── video.mov
        └── Q2
            └── pic.jpeg
        └── Q3
            └── film.mkv
        └── Q4
            └── cat.hevc
"""
USAGE = """
python main.py -s path/to/source -d path/to/destination  <-- To copy media files from source to destination
python main.py -s path/to/directory -ext                 <-- To discover miscellaneous file extensions in directory
"""


def main():
    args = _configure_parser().parse_args(sys.argv[1:])
    DirectoryManager().check_if_directory_exists(args.source)
    DBInitializer(ROOT_DIR).init_prod_database()

    if args.extensions and args.source:
        ExtensionPresenter(args.source).display_misc_extensions()
    elif args.miscellaneous and args.source and args.destination:
        DirectoryManager().check_if_directory_exists(args.destination)
        __run_copy_controller(args, include_misc_files=True)
    elif args.destination and args.source:
        DirectoryManager().check_if_directory_exists(args.destination)
        __run_copy_controller(args, include_misc_files=False)
    else:
        error_message = "Must provide source flag (-s <directory path>) and either -ext flag or " \
                        "-d flag (-d <directory path>)"
        raise argparse.ArgumentError(None, error_message)


def __run_copy_controller(args, include_misc_files):
    CopyController(destination_root_directory=args.destination,
                   source_root_directory=args.source,
                   include_misc_files=include_misc_files).copy_files()


def _configure_parser():
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION, usage=USAGE,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s', '--source', type=str, required=True, help='Source directory path.')
    parser.add_argument('-d', '--destination', type=str, required=False, help='Destination directory path.')
    parser.add_argument('-ext', '--extensions', action='store_true', default=False, required=False,
                        help='Displays miscellaneous extensions in source directory.')
    parser.add_argument('-misc', '--miscellaneous', action='store_true', default=False, required=False,
                        help='Copies miscellaneous files to /<destination directory path>/misc')
    return parser


if __name__ == '__main__':
    main()
