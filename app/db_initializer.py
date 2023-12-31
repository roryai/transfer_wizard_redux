from pathlib import Path as p
import sqlite3

from app.db_controller import DBController


class DBInitializer:

    def __init__(self):
        self.connection = None

    def init_prod_database(self):
        self.__init_database('files_prod')

    def init_test_database(self):
        self.__init_database('files_test')

    def __init_database(self, db_name):
        self.__connection(db_name)
        self.__create_table()

    def __connection(self, db_name):
        db_filepath = self.__db_path(db_name)
        self.connection = sqlite3.connect(db_filepath)

    def __db_path(self, db_name):
        return str(p(__file__).parent.parent) + f'/{db_name}.db'

    def __create_table(self):
        create_files_table = """
             CREATE TABLE IF NOT EXISTS files (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 source_filepath TEXT NOT NULL,
                 destination_filepath TEXT NOT NULL,
                 size INTEGER NOT NULL,
                 copied BOOLEAN,
                 name_clash BOOLEAN
             );
         """
        DBController().set_connection(self.connection).execute_query(create_files_table, [])
