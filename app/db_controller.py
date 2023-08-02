from pathlib import Path
import sqlite3
from sqlite3 import Error


class DBControllerMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(DBControllerMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class DBController(metaclass=DBControllerMeta):

    def __init__(self, db_name='files'):
        self.connection = self.__connection(db_name)

    def __connection(self, db_name):
        db_filepath = self.__db_path(db_name)
        return sqlite3.connect(db_filepath)

    def __db_path(self, db_name):
        return str(Path(__file__).parent.parent) + f'/{db_name}.db'

    def execute_query(self, query, values):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Error as e:
            print(f"Error '{e}' occurred with \nQuery {query}\nValues: {values}")
            raise Error

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
