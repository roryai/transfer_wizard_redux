from app.db_controller import DBController


class FileGateway:

    def __init__(self):
        self.db_controller = DBController()

    def insert(self, file):
        statement = """
            INSERT INTO
                files (source_filepath, destination_filepath, size, copied, name_clash, media, copy_attempted)
            VALUES
                (?, ?, ?, ?, ?, ?, ?);
        """
        values = [file.source_filepath, file.destination_filepath, file.size,
                  file.copied, file.name_clash, file.media, file.copy_attempted]
        return self.db_controller.execute_query(statement, values)

    def update_copied(self, copied, copy_attempted, source_filepath):
        statement = f"""
            UPDATE files
            SET 
                copied = {copied},
                copy_attempted = {copy_attempted}
            WHERE
                source_filepath = '{source_filepath}'
        """
        return self.db_controller.execute_query(statement, [])

    def sum_size(self):
        statement = """
            SELECT SUM(size) 
            FROM files;
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def sum_size_of_files_to_be_copied(self):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE destination_filepath IS NOT NULL
            AND copied == '0'
            AND copy_attempted == '0';
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def count(self):
        statement = """
            SELECT COUNT(*) 
            FROM files;
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def select_all(self):
        statement = """
            SELECT * 
            FROM files;
        """
        return self.db_controller.execute_read_query(statement)

    def select_one_file_where_copy_not_attempted(self):
        statement = """
            SELECT *
            FROM files
            WHERE copied == '0'
            AND copy_attempted == '0'
            AND destination_filepath IS NOT NULL
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
            WHERE destination_filepath IS NULL
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def name_clash_count(self):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE name_clash = '1';
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def wipe_database(self):
        statement = """
            DELETE FROM files;
        """
        return self.db_controller.execute_query(statement, [])
