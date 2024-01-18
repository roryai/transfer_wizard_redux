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

    def select(self, source_filepath):
        statement = f"""
            SELECT * 
            FROM files
            WHERE source_filepath = '{source_filepath}';
        """
        return self.db_controller.execute_read_query(statement, [])[0]

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
        if len(result) == 0:
            return None
        return result[0]

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

    def delete(self, source_filepath):
        statement = f"""
            DELETE FROM files
            WHERE source_filepath = '{source_filepath}';
        """
        return self.db_controller.execute_query(statement, [])

    def wipe_database(self):
        statement = """
            DELETE FROM files;
        """
        return self.db_controller.execute_query(statement, [])

    def count(self):
        statement = """
            SELECT COUNT(*)
            FROM files;
        """
        return self.db_controller.execute_read_query(statement, [])[0][0]

    def duplicate_count(self):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE destination_filepath IS NULL
        """
        return self.db_controller.execute_read_query(statement, [])[0][0]

    def name_clash_count(self):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE name_clash = '1';
        """
        return self.db_controller.execute_read_query(statement, [])[0][0]

    def count_files_by_type(self, media):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE media = ?;
        """
        values = [int(media)]
        return self.db_controller.execute_read_query(statement, values)[0][0]

    def count_media_files(self):
        return self.count_files_by_type(media=True)

    def count_misc_files(self):
        return self.count_files_by_type(media=False)

    def count_name_clash_files_by_type(self, media):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE media = ?
            AND name_clash = '1';
        """
        values = [int(media)]
        return self.db_controller.execute_read_query(statement, values)[0][0]

    def count_name_clash_misc_files(self):
        return self.count_name_clash_files_by_type(media=False)

    def count_name_clash_media_files(self):
        return self.count_name_clash_files_by_type(media=True)

    def count_files_by_copy_status_and_type(self, copied, copy_attempted, media):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE copied = ?
            AND copy_attempted = ?
            AND media = ?;
        """
        values = [int(copied), int(copy_attempted), int(media)]
        return self.db_controller.execute_read_query(statement, values)[0][0]

    def count_copied_misc_files(self):
        return self.count_files_by_copy_status_and_type(copied=True, copy_attempted=True, media=False)

    def count_copied_media_files(self):
        return self.count_files_by_copy_status_and_type(copied=True, copy_attempted=True, media=True)

    def count_uncopied_misc_files(self):
        return self.count_files_by_copy_status_and_type(copied=False, copy_attempted=False, media=False)

    def count_uncopied_media_files(self):
        return self.count_files_by_copy_status_and_type(copied=False, copy_attempted=False, media=True)

    def count_failed_copy_misc_files(self):
        return self.count_files_by_copy_status_and_type(copied=False, copy_attempted=True, media=False)

    def count_failed_copy_media_files(self):
        return self.count_files_by_copy_status_and_type(copied=False, copy_attempted=True, media=True)

    def count_duplicate_files_by_type(self, media):
        statement = """
            SELECT COUNT(*)
            FROM files
            WHERE media = ?
            AND destination_filepath IS NULL;
        """
        values = [int(media)]
        return self.db_controller.execute_read_query(statement, values)[0][0]

    def count_duplicate_media_files(self):
        return self.count_duplicate_files_by_type(media=True)

    def count_duplicate_misc_files(self):
        return self.count_duplicate_files_by_type(media=False)

    def sum_size(self):
        statement = """
            SELECT SUM(size) 
            FROM files;
        """
        return self.db_controller.execute_read_query(statement, [])[0][0]

    def sum_size_of_files_by_type(self, media):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE media = ?;
        """
        values = [int(media)]
        return self.db_controller.execute_read_query(statement, values)[0][0]

    def sum_size_of_media_files(self):
        return self.sum_size_of_files_by_type(media=True)

    def sum_size_of_misc_files(self):
        return self.sum_size_of_files_by_type(media=False)

    def sum_size_of_name_clash_files(self):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE name_clash = '1';
        """
        return self.db_controller.execute_read_query(statement, [])[0][0]

    def sum_size_of_duplicate_files(self):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE destination_filepath IS NULL;
        """
        return self.db_controller.execute_read_query(statement, [])[0][0]

    def sum_size_of_duplicate_files_by_type(self, media):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE destination_filepath IS NULL
            AND media = ?;
        """
        values = [int(media)]
        return self.db_controller.execute_read_query(statement, values)[0][0]

    def sum_size_of_duplicate_media_files(self):
        return self.sum_size_of_duplicate_files_by_type(media=True)

    def sum_size_of_duplicate_misc_files(self):
        return self.sum_size_of_duplicate_files_by_type(media=False)

    def sum_size_of_name_clash_files_by_type(self, media):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE name_clash is '1'
            AND media = ?;
        """
        values = [int(media)]
        return self.db_controller.execute_read_query(statement, values)[0][0]

    def sum_size_of_name_clash_media_files(self):
        return self.sum_size_of_name_clash_files_by_type(media=True)

    def sum_size_of_name_clash_misc_files(self):
        return self.sum_size_of_name_clash_files_by_type(media=False)

    def sum_size_of_files_to_be_copied_by_type(self, media):
        statement = """
            SELECT SUM(size)
            FROM files
            WHERE destination_filepath IS NOT NULL
            AND copied == '0'
            AND copy_attempted == '0'
            AND media = ?
        """
        values = [int(media)]
        return self.db_controller.execute_read_query(statement, values)[0][0]

    def sum_size_of_media_files_to_be_copied(self):
        return self.sum_size_of_files_to_be_copied_by_type(media=True)

    def sum_size_of_misc_files_to_be_copied(self):
        return self.sum_size_of_files_to_be_copied_by_type(media=False)
