from app.file_gateway import FileGateway
from app.logger import Logger


class StatPresenter:

    def __init__(self, source_directory, destination_directory):
        self.source_directory = source_directory
        self.destination_directory = destination_directory
        self.file_gateway = FileGateway()
        self.candidate_file_count = self.__candidate_file_count()
        self.duplicate_file_count = self.__duplicate_file_count()
        self.name_clash_file_count = self.__name_clash_file_count()
        self.to_be_copied_count = self.candidate_file_count - self.duplicate_file_count
        self.stats_summary = self.__build_stats_summary()

    def print_stats_summary(self):
        print(self.stats_summary)

    def log_pre_copy_stats(self):
        Logger().log_to_file(self.stats_summary)

    def __build_stats_summary(self):
        summary = ''
        summary += self.__destination_and_source_path_info()
        summary += '\n'
        summary += self.__candidate_files_info()
        summary += '\n'
        summary += self.__handle_display_of_duplicate_and_name_clash_info()
        summary += self.__to_be_copied_info()
        summary += self.__total_size_of_files_to_be_copied_info()
        return summary

    def __destination_and_source_path_info(self):
        source = f'Source directory: {self.source_directory}'
        destination = f'Destination directory: {self.destination_directory}'
        return f'{source}\n{destination}\n'

    def __candidate_files_info(self):
        file_or_files = self.__file_or_files(self.candidate_file_count)
        candidates = f'{self.candidate_file_count} candidate {file_or_files} discovered in source directory.'
        candidates_size = f'Total size of candidate {file_or_files}: {self.__size_calc(self.file_gateway.sum_size())}MB'
        return f'{candidates}\n{candidates_size}\n'

    def __handle_display_of_duplicate_and_name_clash_info(self):
        summary = ''
        if self.duplicate_file_count > 0:
            summary += self.__duplicate_file_info()
        if self.name_clash_file_count > 0:
            summary += self.__name_clash_file_info()
        if self.duplicate_file_count + self.name_clash_file_count > 0:
            summary += '\n'
        return summary

    def __duplicate_file_info(self):
        single_statement = 'file is a duplicate'
        plural_statement = 'files are duplicates'
        resolved_statement = self.__single_or_plural_grammar(self.duplicate_file_count,
                                                             single_statement, plural_statement)
        return f'{self.duplicate_file_count} {resolved_statement} and will not be copied.\n'

    def __name_clash_file_info(self):
        single_statement = 'file has a name clash'
        plural_statement = 'files have name clashes'
        resolved_statement = self.__single_or_plural_grammar(self.__name_clash_file_count(),
                                                             single_statement, plural_statement)
        return f'{self.name_clash_file_count} {resolved_statement} and will be copied with a unique suffix.\n'

    def __to_be_copied_info(self):
        file_or_files = self.__file_or_files(self.to_be_copied_count)
        return f'{self.to_be_copied_count} {file_or_files} will be copied.\n'

    def __total_size_of_files_to_be_copied_info(self):
        files_to_be_copied_size_sum = self.file_gateway.sum_size_of_files_to_be_copied()
        file_or_files = self.__file_or_files(self.to_be_copied_count)
        return f'Total size of {file_or_files} to be copied: {self.__size_calc(files_to_be_copied_size_sum)}MB\n'

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
