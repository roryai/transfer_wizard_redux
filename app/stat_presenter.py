from app.file_gateway import FileGateway

table_header = '        Discovered         To be copied       Duplicate          Name clash'
table_subheading = '        Count   Size       Count   Size       Count   Size       Count   Size'
divider = '______________________________________________________________________________'
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
            *self._table(),
            footer_info,
            self._total_to_be_copied_count(),
            self._total_to_be_copied_size_sum(),
            ''
        ])

    def _directories_info(self):
        return f"""Source root directory: {self.source_root_directory}
Destination root directory: {self.destination_root_directory}
"""

    def _table(self):
        return [table_header,
                table_subheading,
                divider,
                self._build_row('media'),
                self._build_row('misc'),
                divider,
                self._build_row('total')]

    def _build_row(self, row_name):
        methods = self._switch_methods(row_name)
        return self._format_row(row_name, methods)

    def _switch_methods(self, row_name):
        return self._total_methods() if row_name == 'total' else self._shared_methods(row_name)

    def _total_methods(self):
        return [self._total_size_methods(), self._total_count_methods()]

    def _shared_methods(self, row_name):
        return [self._construct_size_methods(row_name), self._construct_count_methods(row_name)]

    def _total_size_methods(self):
        return [FileGateway.sum_size, FileGateway.sum_size_of_files_to_be_copied,
                FileGateway.sum_size_of_duplicate_files, FileGateway.sum_size_of_name_clash_files]

    def _total_count_methods(self):
        return [FileGateway.count, FileGateway.count_files_to_be_copied,
                FileGateway.duplicate_count, FileGateway.name_clash_count]

    def _construct_count_methods(self, file_type):
        return [getattr(FileGateway, f'count_{file_type}_files'),
                getattr(FileGateway, f'count_{file_type}_files_to_be_copied'),
                getattr(FileGateway, f'count_duplicate_{file_type}_files'),
                getattr(FileGateway, f'count_name_clash_{file_type}_files')]

    def _construct_size_methods(self, file_type):
        return [getattr(FileGateway, f'sum_size_of_{file_type}_files'),
                getattr(FileGateway, f'sum_size_of_{file_type}_files_to_be_copied'),
                getattr(FileGateway, f'sum_size_of_duplicate_{file_type}_files'),
                getattr(FileGateway, f'sum_size_of_name_clash_{file_type}_files')]

    def _format_row(self, row_name, methods):
        discovered_size, to_be_copied_size, duplicate_size, name_clash_size = \
            self._padded_data(methods[0], self._megabyte_padder)
        discovered_count, to_be_copied_count, duplicate_count, name_clash_count = \
            self._padded_data(methods[1], self._padder)
        row_label = self._padder(row_name.capitalize())
        return f'{row_label}{discovered_count}{discovered_size}{to_be_copied_count}{to_be_copied_size}' \
               f'{duplicate_count}{duplicate_size}{name_clash_count}{name_clash_size}'

    def _total_to_be_copied_count(self):
        count = self.gateway.count_files_to_be_copied()
        file_or_files = 'file' if count == 1 else 'files'
        return f'{count} {file_or_files}'

    def _total_to_be_copied_size_sum(self):
        size = self.gateway.sum_size_of_files_to_be_copied()
        return self._format_size(size)

    def _padded_data(self, methods, padder):
        return [padder(method(self.gateway)) for method in methods]

    def _megabyte_padder(self, bytes):
        megabytes = self._convert_bytes_to_megabytes(bytes)
        spaces_count = 9 - len(str(megabytes))
        spaces = ' ' * spaces_count
        return f'{megabytes}MB{spaces}'

    def _padder(self, val):
        spaces_count = 8 - len(str(val))
        spaces = ' ' * spaces_count
        return f'{val}{spaces}'

    def _format_size(self, size):
        return f'{self._convert_bytes_to_megabytes(size)}MB'

    def _convert_bytes_to_megabytes(self, sum_size):
        if sum_size is None:
            return 0.0
        return round(sum_size / 1048576, 2)
