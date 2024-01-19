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
        print(self.__build_stat_summary())

    def __build_stat_summary(self):
        return '\n'.join([
            self.__directories(),
            table_header,
            table_subheading,
            divider,
            self.__build_row('media'),
            self.__build_row('misc'),
            divider,
            self.__build_row('total'),
            footer_info,
            self.__total_to_be_copied_count(),
            self.__total_to_be_copied_size_sum()
        ])

    def __directories(self):
        return f"""Source root directory: {self.source_root_directory}
Destination root directory: {self.destination_root_directory}
"""

    def __build_row(self, row_name):
        methods = self.__switch_methods(row_name)
        return self.__format_row(row_name, methods)

    def __switch_methods(self, row_name):
        return self.__total_methods() if row_name == 'total' else self.__shared_methods(row_name)

    def __total_methods(self):
        return [self.__total_size_methods(), self.__total_count_methods()]

    def __shared_methods(self, row_name):
        return [self.__construct_size_methods(row_name), self.__construct_count_methods(row_name)]

    def __total_size_methods(self):
        return [FileGateway.sum_size, FileGateway.sum_size_of_files_to_be_copied,
                FileGateway.sum_size_of_duplicate_files, FileGateway.sum_size_of_name_clash_files]

    def __total_count_methods(self):
        return [FileGateway.count, FileGateway.count_files_to_be_copied,
                FileGateway.duplicate_count, FileGateway.name_clash_count]

    def __construct_count_methods(self, file_type):
        return [getattr(FileGateway, f'count_{file_type}_files'),
                getattr(FileGateway, f'count_{file_type}_files_to_be_copied'),
                getattr(FileGateway, f'count_duplicate_{file_type}_files'),
                getattr(FileGateway, f'count_name_clash_{file_type}_files')]

    def __construct_size_methods(self, file_type):
        return [getattr(FileGateway, f'sum_size_of_{file_type}_files'),
                getattr(FileGateway, f'sum_size_of_{file_type}_files_to_be_copied'),
                getattr(FileGateway, f'sum_size_of_duplicate_{file_type}_files'),
                getattr(FileGateway, f'sum_size_of_name_clash_{file_type}_files')]

    def __format_row(self, row_name, methods):
        discovered_size, to_be_copied_size, duplicate_size, name_clash_size = \
            self.__padded_data(methods[0], self.__megabyte_padder)
        discovered_count, to_be_copied_count, duplicate_count, name_clash_count = \
            self.__padded_data(methods[1], self.__padder)
        row_label = self.__padder(row_name.capitalize())
        return f'{row_label}{discovered_count}{discovered_size}{to_be_copied_count}{to_be_copied_size}' \
               f'{duplicate_count}{duplicate_size}{name_clash_count}{name_clash_size}'

    def __total_to_be_copied_count(self):
        count = self.gateway.count_files_to_be_copied()
        file_or_files = 'file' if count == 1 else 'files'
        return f'{count} {file_or_files}'

    def __total_to_be_copied_size_sum(self):
        size = self.gateway.sum_size_of_files_to_be_copied()
        return self.__format_size(size)

    def __padded_data(self, methods, padder):
        return [padder(method(self.gateway)) for method in methods]

    def __megabyte_padder(self, bytes):
        megabytes = self.__convert_bytes_to_megabytes(bytes)
        spaces_count = 9 - len(str(megabytes))
        spaces = ' ' * spaces_count
        return f'{megabytes}MB{spaces}'

    def __padder(self, val):
        spaces_count = 8 - len(str(val))
        spaces = ' ' * spaces_count
        return f'{val}{spaces}'

    def __format_size(self, size):
        return f'{self.__convert_bytes_to_megabytes(size)}MB'

    def __convert_bytes_to_megabytes(self, sum_size):
        if sum_size is None:
            return 0.0
        return round(sum_size / 1048576, 2)
