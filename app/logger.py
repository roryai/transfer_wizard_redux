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

    def init_log_file(self, destination_root_directory):
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M.%S')
        suffix = '_media_transfer_logfile.txt'
        filename = f'{timestamp}{suffix}'
        log_file_path = os.path.join(destination_root_directory, filename)

        open(log_file_path, 'w').close()

        self.log_file_path = log_file_path

    def log_successful_copy(self, source_file_path, destination_filepath):
        log_entry = f'Copy succeeded: {source_file_path} copied to {destination_filepath}'
        self._append_to_logfile(log_entry)
        self.successful_copy_count += 1

    def log_unsuccessful_copy(self, source_file_path, destination_filepath):
        log_entry = f'Copy failed:    {source_file_path} not copied to {destination_filepath}'
        self._append_to_logfile(log_entry)
        self.unsuccessful_copy_count += 1

    def log_duplicate(self, filepath_1, filepath_2):
        log_entry = f'Duplicate:      {filepath_1} identical to {filepath_2}'
        self._append_to_logfile(log_entry)

    def log_name_clash(self, source_filepath, destination_filepath):
        log_entry = f'Name clash:     {source_filepath} clashes with {destination_filepath}'
        self._append_to_logfile(log_entry)

    def log_error(self, message, error, values):
        message = f'Context: {message}\nError: {error}\nValues: {values}\n'
        self.error_messages.append(message)

    def append_errors_to_logfile(self):
        self.combined_error_messages = '\n'.join(self.error_messages)
        self._append_to_logfile(f'\nErrors:\n{self.combined_error_messages}')

    def append_summary_to_file(self):
        file_or_files_succeeded = self._file_or_files(self.successful_copy_count)
        file_or_files_failed = self._file_or_files(self.unsuccessful_copy_count)
        summary = f"""
{self.successful_copy_count} {file_or_files_succeeded} copied successfully
{self.unsuccessful_copy_count} {file_or_files_failed} failed to copy"""
        self._append_to_logfile(summary)

    def log_to_file(self, log_entry):
        self._append_to_logfile(log_entry)

    def _append_to_logfile(self, log_entry):
        with open(self.log_file_path, 'a') as file:
            file.write(f'{log_entry}\n')

    def _file_or_files(self, count):
        return 'file' if count == 1 else 'files'
