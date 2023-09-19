from app.db_controller import DBController


class FileGateway:

    def __init__(self):
        self.db_controller = DBController()

    def insert(self, file):
        statement = f"""
            INSERT INTO
                files (source_filepath, target_filepath, size, name_clash)
            VALUES
                (?, ?, ?, ?);
        """
        values = [file.source_filepath, file.target_filepath, file.size, file.name_clash]
        return self.db_controller.execute_query(statement, values)

    def sum_size(self):
        statement = f"""
            SELECT SUM(size) 
            FROM files;
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def count(self):
        statement = f"""
            SELECT COUNT(*) 
            FROM files;
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def select_all(self):
        statement = f"""
            SELECT * 
            FROM files;
        """
        return self.db_controller.execute_read_query(statement)

    def duplicate_count(self):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE target_filepath = '';
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def name_clashes_count(self):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE name_clash = '1';
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def wipe_database(self):
        statement = f"""
            DELETE FROM files;
        """
        return self.db_controller.execute_query(statement, [])
