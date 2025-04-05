import os
import sqlite3

from app.db_controller import DBController


class DBInitializer:

    def __init__(self, project_root):
        self.connection = None
        self.project_root = project_root

    def init_prod_database(self):
        self._init_database('files_prod')

    def init_test_database(self):
        self._init_database('files_test')

    def _init_database(self, db_name):
        self._connection(db_name)
        self._create_table()

    def _connection(self, db_name):
        db_filepath = self._db_path(db_name)
        self.connection = sqlite3.connect(db_filepath)

    def _db_path(self, db_name):
        db_filename = f'{db_name}.db'
        return os.path.join(self.project_root, db_filename)

    def _create_table(self):
        create_files_table = """
             CREATE TABLE IF NOT EXISTS files (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 source_filepath TEXT NOT NULL UNIQUE,
                 destination_filepath TEXT UNIQUE,
                 size INTEGER NOT NULL,
                 copied BOOLEAN NOT NULL,
                 name_clash BOOLEAN NOT NULL,
                 copy_attempted BOOLEAN NOT NULL
             );
         """
        DBController().set_connection(self.connection).execute_query(create_files_table, [])
