from app.db_controller import DBController


class FileGateway:

    def __init__(self):
        self.db_controller = DBController()

    def insert(self, file):
        statement = f"""
            INSERT INTO
                files (source_filepath, target_filepath, size)
            VALUES
                (?, ?, ?);
        """
        values = [file.source_filepath, file.target_filepath, file.size]
        return self.db_controller.execute_query(statement, values)

    def sum_size(self):
        statement = f"""
            SELECT SUM(size) from files;
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def count(self):
        statement = f"""
            SELECT COUNT(*) from files;
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def select_all(self):
        statement = f"""
            SELECT * FROM files;
        """
        return self.db_controller.execute_read_query(statement)

    def delete_all(self):
        statement = f"""
            DELETE FROM files;
        """
        return self.db_controller.execute_query(statement, [])