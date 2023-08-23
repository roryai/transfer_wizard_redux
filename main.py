import argparse

from app.app_controller import AppController
from app.db_initializer import DBInitializer


def main(source_directory, target_directory):
    DBInitializer().init_prod_database()
    AppController(source_directory, target_directory).run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This program copies media files to an organised directory structure.')
    parser.add_argument('-s', '--source', type=str, required=True)
    parser.add_argument('-t', '--target', type=str, required=True)
    args = parser.parse_args()
    main(args.source, args.target)
