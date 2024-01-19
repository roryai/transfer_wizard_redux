from datetime import datetime
import os
import sys


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
        self.successful_copy_count = 0
        self.unsuccessful_copy_count = 0
        self.exit_message = """
Error limit reached. Check logfile for full details.

Errors:
"""

    def init_log_file(self, destination_root_directory):
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M.%S')
        suffix = '_media_transfer_logfile.txt'
        filename = f'{timestamp}{suffix}'
        log_file_path = os.path.join(destination_root_directory, filename)

        open(log_file_path, 'w').close()

        self.log_file_path = log_file_path

    def log_successful_copy(self, source_file_path, destination_filepath):
        log_entry = f'Copy succeeded: {source_file_path} copied to {destination_filepath}'
        self.__append_to_logfile(log_entry)
        self.successful_copy_count += 1

    def log_unsuccessful_copy(self, source_file_path, destination_filepath):
        log_entry = f'Copy failed:    {source_file_path} not copied to {destination_filepath}'
        self.__append_to_logfile(log_entry)
        self.unsuccessful_copy_count += 1

    def log_error(self, error, values):
        message = f'Error: {error}. Values: {values}'
        self.error_messages.append(message)
        if len(self.error_messages) > 2:
            self.exit_message += '\n'.join(self.error_messages)
            print(self.exit_message)
            sys.exit()

    def append_errors_to_logfile(self):
        self.combined_error_messages = '\n'.join(self.error_messages)
        self.__append_to_logfile(f'\nErrors:\n{self.combined_error_messages}')

    def append_summary_to_file(self):
        file_or_files_succeeded = self.__file_or_files(self.successful_copy_count)
        file_or_files_failed = self.__file_or_files(self.unsuccessful_copy_count)
        summary = f"""
{self.successful_copy_count} {file_or_files_succeeded} copied successfully
{self.unsuccessful_copy_count} {file_or_files_failed} failed to copy"""
        self.__append_to_logfile(summary)

    def log_to_file(self, log_entry):
        self.__append_to_logfile(log_entry)

    def __append_to_logfile(self, log_entry):
        with open(self.log_file_path, 'a') as file:
            file.write(f'{log_entry}\n')

    def __file_or_files(self, count):
        return 'file' if count == 1 else 'files'
