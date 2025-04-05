from app.file_gateway import FileGateway

table_header = 'Discovered         To be copied       Duplicate          Name clash'
table_subheading = 'Count   Size       Count   Size       Count   Size       Count   Size'
divider = '____________________________________________________________________________'
footer_info = """
Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:"""


class StatPresenter:

    def __init__(self, source_root_directory, destination_root_directory):
        self.source_root_directory = source_root_directory
        self.destination_root_directory = destination_root_directory
        self.gateway = FileGateway()

    def print_stats_summary(self):
        summary = self._build_stat_summary()
        print(self._build_stat_summary())
        return summary

    def _build_stat_summary(self):
        return '\n'.join([
            self._directories_info(),
            table_header,
            table_subheading,
            divider,
            self._data_row(),
            footer_info,
            self._to_be_copied_count(),
            self._to_be_copied_size_sum(),
            ''
        ])

    def _directories_info(self):
        return f"""Source root directory: {self.source_root_directory}
Destination root directory: {self.destination_root_directory}
"""

    def _data_row(self):
        discovered_size, to_be_copied_size, duplicate_size, name_clash_size = \
            self._padded_data(self._size_methods(), self._megabyte_padder)
        discovered_count, to_be_copied_count, duplicate_count, name_clash_count = \
            self._padded_data(self._count_methods(), self._count_padder)
        return f'{discovered_count}{discovered_size}{to_be_copied_count}{to_be_copied_size}' \
               f'{duplicate_count}{duplicate_size}{name_clash_count}{name_clash_size}'

    def _size_methods(self):
        return [FileGateway.sum_size, FileGateway.sum_size_of_files_to_be_copied,
                FileGateway.sum_size_of_duplicate_files, FileGateway.sum_size_of_name_clash_files]

    def _count_methods(self):
        return [FileGateway.count, FileGateway.count_files_to_be_copied,
                FileGateway.duplicate_count, FileGateway.name_clash_count]

    def _to_be_copied_count(self):
        count = self.gateway.count_files_to_be_copied()
        file_or_files = 'file' if count == 1 else 'files'
        return f'{count} {file_or_files}'

    def _to_be_copied_size_sum(self):
        size = self.gateway.sum_size_of_files_to_be_copied()
        return self._format_size(size)

    def _padded_data(self, methods, padder):
        return [padder(method(self.gateway)) for method in methods]

    def _megabyte_padder(self, bytes):
        megabytes = self._convert_bytes_to_megabytes(bytes)
        spaces_count = 9 - len(str(megabytes))
        spaces = ' ' * spaces_count
        return f'{megabytes}MB{spaces}'

    def _count_padder(self, val):
        spaces_count = 8 - len(str(val))
        spaces = ' ' * spaces_count
        return f'{val}{spaces}'

    def _format_size(self, size):
        return f'{self._convert_bytes_to_megabytes(size)}MB'

    def _convert_bytes_to_megabytes(self, sum_size):
        if sum_size is None:
            return 0.0
        return round(sum_size / 1048576, 2)
