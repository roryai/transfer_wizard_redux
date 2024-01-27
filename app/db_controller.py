import sqlite3
from sqlite3 import Error

from app.logger import Logger


class DBControllerMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(DBControllerMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class DBController(metaclass=DBControllerMeta):

    def __init__(self):
        self.connection = None

    def set_connection(self, connection):
        self.connection = connection
        return self

    def execute_query(self, query, values):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Error as e:
            Logger().log_error('Error in DBController', e, values)

    def execute_read_query(self, query, values):
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        return result
