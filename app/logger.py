from datetime import datetime
import os


class LoggerMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(LoggerMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class Logger(metaclass=LoggerMeta):

    def __init__(self):
        self.log_file_path = None
        self.error_messages = []
        self.combined_error_messages = ''

    def init_log_file(self, destination_directory):
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M.%S')
        suffix = 'media_transfer_logfile.txt'
        filename = timestamp + suffix
        log_file_path = os.path.join(destination_directory, filename)

        with open(log_file_path, 'w'):
            pass

        self.log_file_path = log_file_path

    def log_successful_copy(self, source_file_path, destination_filepath):
        log_entry = f'Copy succeeded: {source_file_path} copied to {destination_filepath}'
        self.__write_to_logfile(log_entry)

    def log_unsuccessful_copy(self, source_file_path, destination_filepath):
        log_entry = f'Copy failed:    {source_file_path} not copied to {destination_filepath}'
        self.__write_to_logfile(log_entry)

    def log_error(self, error, values):
        message = f'Error: {error}. Values: {values}'
        self.error_messages.append(message)

    def write_errors_to_logfile(self):
        heading = '\nErrors:\n'
        self.combined_error_messages = '\n'.join(self.error_messages)
        self.__write_to_logfile(heading + self.combined_error_messages)

    def __write_to_logfile(self, log_entry):
        with open(self.log_file_path, 'a') as file:
            file.write(f'{log_entry}\n')