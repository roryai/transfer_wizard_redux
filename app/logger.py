from datetime import datetime
import os


class Logger:

    def __init__(self, destination_directory):
        self.log_file_path = self.__init_log_file(destination_directory)

    def log_successful_copy(self, source_file_path, destination_filepath):
        log_entry = f'Copy succeeded: {source_file_path} copied to {destination_filepath}'
        self.__write_to_logfile(log_entry)

    def log_unsuccessful_copy(self, source_file_path, destination_filepath):
        log_entry = f'Copy failed:    {source_file_path} not copied to {destination_filepath}'
        self.__write_to_logfile(log_entry)

    def __init_log_file(self, destination_directory):
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M.%S')
        suffix = 'media_transfer_logfile.txt'
        filename = timestamp + suffix
        log_file_path = os.path.join(destination_directory, filename)

        with open(log_file_path, 'w'):
            pass

        return log_file_path

    def __write_to_logfile(self, log_entry):
        with open(self.log_file_path, 'a') as file:
            file.write(f'{log_entry}\n')
