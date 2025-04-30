from app.db_controller import DBController


class FileGateway:

    def __init__(self):
        self.db_controller = DBController()

    def execute_query(self, statement, values=None):
        values = values or []
        return self.db_controller.execute_query(statement, values)

    def execute_read_query(self, statement, values=None):
        values = values or []
        return self.min_size_zero(self.db_controller.execute_read_query(statement, values)[0][0])

    def min_size_zero(self, result):
        return 0 if not result else result

    def insert(self, file):
        statement = """
            INSERT INTO
                files (source_filepath, destination_filepath, size, copied, name_clash, copy_attempted)
            VALUES
                (?, ?, ?, ?, ?, ?);
        """
        values = [file.source_filepath, file.destination_filepath, file.size,
                  file.copied, file.name_clash, file.copy_attempted]
        return self.db_controller.execute_query(statement, values)

    def select(self, source_filepath):
        statement = f"""
            SELECT * 
            FROM files
            WHERE source_filepath = ?;
        """
        return self.db_controller.execute_read_query(statement, [source_filepath])[0]

    def select_one_where_copy_not_attempted(self):
        statement = """
            SELECT *
            FROM files
            WHERE copied == '0'
            AND copy_attempted == '0'
            AND destination_filepath IS NOT NULL
            LIMIT 1;
        """
        result = self.db_controller.execute_read_query(statement, [])
        return None if len(result) == 0 else result[0]

    def update_copied(self, copied, copy_attempted, source_filepath):
        statement = f"""
            UPDATE files
            SET 
                copied = ?,
                copy_attempted = ?
            WHERE
                source_filepath = ?
        """
        values = [copied, copy_attempted, source_filepath]
        return self.execute_query(statement, values)

    def delete(self, source_filepath):
        statement = f"""
            DELETE FROM files
            WHERE source_filepath = ?;
        """
        return self.execute_query(statement, [source_filepath])

    def wipe_database(self):
        statement = """
            DELETE FROM files;
        """
        return self.execute_query(statement)

    def count(self):
        statement = """
            SELECT COUNT(*)
            FROM files;
        """
        return self.execute_read_query(statement)

    def count_files_to_be_copied(self):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE destination_filepath IS NOT NULL
            AND copied = '0'
            AND copy_attempted = '0';
        """
        return self.execute_read_query(statement, [])

    def duplicate_count(self):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE destination_filepath IS NULL
        """
        return self.execute_read_query(statement)

    def name_clash_count(self):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE name_clash = '1';
        """
        return self.execute_read_query(statement)

    def destination_filepath_in_use(self, destination_filepath):
        statement = """
                    SELECT COUNT(*)
                    FROM files
                    WHERE destination_filepath = ?;
                """
        values = [destination_filepath]
        result = self.execute_read_query(statement, values)
        return bool(result)

    def select_duplicate_file(self, destination_filepath, size):
        statement = f"""
                    SELECT * 
                    FROM files
                    WHERE destination_filepath = ?
                    AND size = ?;
                """
        values = [destination_filepath, size]
        return self.db_controller.execute_read_query(statement, values)[0]

    def identical_size_and_destination_filepath_record_exists(self, destination_filepath, size):
        statement = """
                    SELECT COUNT(*)
                    FROM files
                    WHERE destination_filepath = ?
                    AND size = ?;
                """
        values = [destination_filepath, size]
        result = self.execute_read_query(statement, values)
        return bool(result)

    def sum_size(self):
        statement = """
            SELECT SUM(size) 
            FROM files;
        """
        return self.execute_read_query(statement)

    def sum_size_of_name_clash_files(self):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE name_clash = '1';
        """
        return self.execute_read_query(statement)

    def sum_size_of_duplicate_files(self):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE destination_filepath IS NULL;
        """
        return self.execute_read_query(statement)

    def sum_size_of_files_to_be_copied(self):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE destination_filepath IS NOT NULL
            AND copied == '0'
            AND copy_attempted == '0';
        """
        return self.execute_read_query(statement)
