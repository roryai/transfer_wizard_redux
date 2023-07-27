import argparse
import os

from app.scanner import Scanner
from app.transfer import Transfer


def main(source_directory, target_directory):
    for path in [source_directory, target_directory]:
        if not os.path.isdir(path):
            raise FileNotFoundError(f'{path} is not a valid directory.')

    source_directory = __sanitise_filepath(source_directory)
    target_directory = __sanitise_filepath(target_directory)

    filepaths = Scanner().scan_dirs(source_directory)

    for path in filepaths:
        try:
            Transfer().copy_files(path, target_directory)
        except StopIteration:
            break


def __sanitise_filepath(filepath):
    if filepath[-1] != '/':
        filepath += '/'
    return filepath


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This program copies media files to an organised directory structure.')
    parser.add_argument('-s', '--source', type=str, required=True)
    parser.add_argument('-t', '--target', type=str, required=True)
    args = parser.parse_args()
    main(args.source, args.target)
