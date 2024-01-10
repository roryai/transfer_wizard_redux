from app.db_controller import DBController


class FileGateway:

    def __init__(self):
        self.db_controller = DBController()

    def insert(self, file):
        statement = """
            INSERT INTO
                files (source_filepath, destination_filepath, size, name_clash, media)
            VALUES
                (?, ?, ?, ?, ?);
        """
        values = [file.source_filepath, file.destination_filepath, file.size,
                  file.name_clash, file.media]
        return self.db_controller.execute_query(statement, values)

    def update_copied(self, file):
        # TODO size can be removed from the query now that source_filepath is unique
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
        statement = """
            SELECT SUM(size) 
            FROM files;
        """
        return self.db_controller.execute_read_query(statement)[0][0]

    def sum_size_of_files_to_be_copied(self):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE destination_filepath IS NOT NULL;
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
        # TODO change copied IS NULL to is false after copy set to not null. Keep destination_filepath IS NOT NULL
        statement = """
            SELECT *
            FROM files
            WHERE copied IS NULL
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
