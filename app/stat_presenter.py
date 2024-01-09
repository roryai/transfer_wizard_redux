from app.file_gateway import FileGateway


class StatPresenter:

    def __init__(self, source_directory, destination_directory):
        self.source_directory = source_directory
        self.destination_directory = destination_directory
        self.file_gateway = FileGateway()
        self.candidate_file_count = self.__candidate_file_count()
        self.duplicate_file_count = self.__duplicate_file_count()
        self.name_clash_file_count = self.__name_clash_file_count()
        self.to_be_copied_count = self.candidate_file_count - self.duplicate_file_count

    def present_analysis_of_candidate_files(self):
        self.__print_destination_and_source_path_info()
        print()
        self.__print_candidate_files_info()
        print()
        self.__handle_display_of_duplicate_and_name_clash_info()
        self.__print_to_be_copied_info()
        self.__print_total_size_of_files_to_be_copied_info()

    def __print_destination_and_source_path_info(self):
        print(f'Source directory: {self.source_directory}')
        print(f'Destination directory: {self.destination_directory}')

    def __print_candidate_files_info(self):
        file_or_files = self.__file_or_files(self.candidate_file_count)
        print(f'{self.candidate_file_count} candidate {file_or_files} discovered in source directory.')
        print(f'Total size of candidate {file_or_files}: {self.__size_calc(self.file_gateway.sum_size())}MB')

    def __handle_display_of_duplicate_and_name_clash_info(self):
        if self.duplicate_file_count > 0:
            self.__print_duplicate_file_info()
        if self.name_clash_file_count > 0:
            self.__print_name_clash_file_info()
        if self.duplicate_file_count + self.name_clash_file_count > 0:
            print()

    def __print_duplicate_file_info(self):
        single_statement = 'file is a duplicate'
        plural_statement = 'files are duplicates'
        resolved_statement = self.__single_or_plural_grammar(self.duplicate_file_count,
                                                             single_statement, plural_statement)
        print(f'{self.duplicate_file_count} {resolved_statement} and will not be copied.')

    def __print_name_clash_file_info(self):
        single_statement = 'file has a name clash'
        plural_statement = 'files have name clashes'
        resolved_statement = self.__single_or_plural_grammar(self.__name_clash_file_count(),
                                                             single_statement, plural_statement)
        print(f'{self.name_clash_file_count} {resolved_statement} and will be copied with a unique suffix.')

    def __print_to_be_copied_info(self):
        file_or_files = self.__file_or_files(self.to_be_copied_count)
        print(f'{self.to_be_copied_count} {file_or_files} will be copied.')

    def __print_total_size_of_files_to_be_copied_info(self):
        files_to_be_copied_size_sum = self.file_gateway.sum_size_of_files_to_be_copied()
        file_or_files = self.__file_or_files(self.to_be_copied_count)
        print(f'Total size of {file_or_files} to be copied: {self.__size_calc(files_to_be_copied_size_sum)}MB')

    def __file_or_files(self, count):
        single_statement = 'file'
        plural_statement = 'files'
        return self.__single_or_plural_grammar(count, single_statement, plural_statement)

    def __size_calc(self, sum_size):
        if sum_size is None:
            return 0.0
        return round(sum_size / 1048576, 2)

    def __single_or_plural_grammar(self, count, single_statement, plural_statement):
        if count == 1:
            return f'{single_statement}'
        else:
            return f'{plural_statement}'

    def __candidate_file_count(self):
        return self.file_gateway.count()

    def __duplicate_file_count(self):
        return self.file_gateway.duplicate_count()

    def __name_clash_file_count(self):
        return self.file_gateway.name_clashes_count()
