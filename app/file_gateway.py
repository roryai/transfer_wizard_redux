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

    def update_copied(self, file):
        statement = f"""
            UPDATE files
            SET 
                copied = {file.copied}
            WHERE
                source_filepath = '{file.source_filepath}'
                AND size = '{file.size}'
        """
        return self.db_controller.execute_query(statement, [])

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

    def select_one_file_where_copy_not_attempted(self):
        statement = f"""
            SELECT *
            FROM files
            WHERE copied IS NULL
            AND target_filepath IS NOT ''
            LIMIT 1;
        """
        result = self.db_controller.execute_read_query(statement)
        if len(result) == 0:
            return None
        return result[0]

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
