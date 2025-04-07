import argparse
import pathlib
import sys

from app.copy_controller import CopyController
from app.db_initializer import DBInitializer
from app.directory_manager import DirectoryManager
from app.mode_flags import ModeFlags

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
PROGRAM_DESCRIPTION = """
This program copies photos and videos to directory structure based on capture date:

└── destination_directory
    └── 2024
        └── Q1
            └── video.mov
        └── Q2
            └── pic.jpg
        └── Q3
            └── film.mkv
        └── Q4
            └── cat.hevc
"""
USAGE = """
python main.py -s path/to/source -d path/to/destination  <-- To copy media files from source to destination
"""


def main():
    args = _configure_parser().parse_args(sys.argv[1:])
    DirectoryManager().check_if_directory_exists(args.source)
    DirectoryManager().check_if_directory_exists(args.destination)
    DBInitializer(ROOT_DIR).init_prod_database()
    if args.year:
        ModeFlags(year_mode=True)
    CopyController(args.destination, args.source).copy_files()


def _configure_parser():
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION, usage=USAGE,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s', '--source', type=str, required=True, help='Source directory path.')
    parser.add_argument('-d', '--destination', type=str, required=True, help='Destination directory path.')
    parser.add_argument('-y', '--year', action='store_true', default=False, required=False,
                        help='Year based destination directories.')
    return parser


if __name__ == '__main__':
    main()
