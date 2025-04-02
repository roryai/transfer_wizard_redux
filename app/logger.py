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

    def log_to_file(self, log_entry):
        self._append_to_logfile(log_entry)

    def finalise_logging(self):
        self._append_summary_to_file()
        print(self._format_error_messages()) if self.error_messages else print("No errors")

    def _append_summary_to_file(self):
        success_count = self._file_or_files(self.successful_copy_count)
        failure_count = self._file_or_files(self.unsuccessful_copy_count)
        error_messages = self._format_error_messages()
        summary = f"""
{self.successful_copy_count} {success_count} copied successfully
{self.unsuccessful_copy_count} {failure_count} failed to copy
Errors:\n{error_messages}"""
        self._append_to_logfile(summary)

    def _append_to_logfile(self, log_entry):
        with open(self.log_file_path, 'a') as file:
            file.write(f'{log_entry}\n')

    def _file_or_files(self, count):
        return 'file' if count == 1 else 'files'

    def _format_error_messages(self):
        return '\n'.join(self.error_messages)
