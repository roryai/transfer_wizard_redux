from app.file_gateway import FileGateway


class StatPresenter:

    def __init__(self, source_root_directory, destination_root_directory):
        self.source_root_directory = source_root_directory
        self.destination_root_directory = destination_root_directory
        self.gateway = FileGateway()
        self.candidate_file_count = self.__candidate_file_count()
        self.duplicate_file_count = self.__duplicate_file_count()
        self.name_clash_file_count = self.__name_clash_file_count()
        self.files_to_be_copied_size_sum = self.__files_to_be_copied_size_sum()
        self.to_be_copied_count = self.candidate_file_count - self.duplicate_file_count
        self.stats_summary = self.__build_stats_summary()

    def print_stats_summary(self):
        print(self.stats_summary)
        return self.stats_summary

    def __build_stats_summary(self):
        if self.to_be_copied_count == 0:
            return self.__no_files_to_copy_message()
        else:
            return self.__files_to_copy_message()

    def __no_files_to_copy_message(self):
        return '\n'.join([
            self.__destination_and_source_path_info(),
            'No files found in source directory'
        ])

    def __files_to_copy_message(self):
        return '\n'.join([
            self.__destination_and_source_path_info(),
            self.__candidate_files_info(),
            self.__filetype_info(),
            self.__handle_display_of_duplicate_and_name_clash_info(),
            self.__to_be_copied_info(),
            self.__total_size_of_files_to_be_copied_info()
        ])

    def __destination_and_source_path_info(self):
        source = f'Source root directory: {self.source_root_directory}'
        destination = f'Destination root directory: {self.destination_root_directory}'
        return f'{source}\n{destination}\n'

    def __candidate_files_info(self):
        file_or_files = self.__file_or_files(self.candidate_file_count)
        candidates = f'{self.candidate_file_count} candidate {file_or_files} discovered in source directory.'
        candidates_size = f'Total size of candidate {file_or_files}: {self.__convert_bytes_to_megabytes(self.gateway.sum_size())}MB'
        return f'{candidates}\n{candidates_size}\n'

    def __filetype_info(self):
        info = ''
        info += self.__media_file_info() if self.__media_file_info() else ''
        info += '\n' if self.__media_file_info() and self.__misc_file_info() else ''
        info += self.__misc_file_info() if self.__misc_file_info() else ''
        return info

    def __media_file_info(self):
        media_file_count = self.gateway.count_uncopied_media_files()
        if media_file_count == 0:
            return ''
        media_file_or_files = self.__single_or_plural_grammar(media_file_count,
                                                              'file is a media file', 'files are media files')
        media_files_size = self.__convert_bytes_to_megabytes(self.gateway.sum_size_of_media_files_to_be_copied())
        return f'{media_file_count} {media_file_or_files}: {media_files_size}MB'

    def __misc_file_info(self):
        misc_file_count = self.gateway.count_uncopied_misc_files()
        if misc_file_count == 0:
            return ''
        misc_file_or_files = self.__single_or_plural_grammar(misc_file_count,
                                                             'file is a miscellaneous file',
                                                             'files are miscellaneous files')
        misc_files_size = self.__convert_bytes_to_megabytes(self.gateway.sum_size_of_misc_files_to_be_copied())
        return f'{misc_file_count} {misc_file_or_files}: {misc_files_size}MB'

    def __handle_display_of_duplicate_and_name_clash_info(self):
        summary = '\n' if self.duplicate_file_count + self.name_clash_file_count > 0 else ''
        summary += f'{self.__duplicate_file_info()}\n' if self.duplicate_file_count > 0 else ''
        summary += f'{self.__name_clash_file_info()}\n' if self.name_clash_file_count > 0 else ''
        return summary

    def __duplicate_file_info(self):
        resolved_statement = self.__single_or_plural_grammar(self.duplicate_file_count,
                                                             'file is a duplicate', 'files are duplicates')
        return f'{self.duplicate_file_count} {resolved_statement} and will not be copied.'

    def __name_clash_file_info(self):
        resolved_statement = self.__single_or_plural_grammar(self.name_clash_file_count,
                                                             'file has a name clash', 'files have name clashes')
        return f'{self.name_clash_file_count} {resolved_statement} and will be copied with a unique suffix.'

    def __to_be_copied_info(self):
        file_or_files = self.__file_or_files(self.to_be_copied_count)
        return f'{self.to_be_copied_count} {file_or_files} will be copied.'

    def __total_size_of_files_to_be_copied_info(self):
        file_or_files = self.__file_or_files(self.to_be_copied_count)
        total_size = self.__convert_bytes_to_megabytes(self.files_to_be_copied_size_sum)
        return f'Total size of {file_or_files} to be copied: {total_size}MB'

    def __file_or_files(self, count):
        return self.__single_or_plural_grammar(count, 'file', 'files')

    def __convert_bytes_to_megabytes(self, sum_size):
        if sum_size is None:
            return 0.0
        return round(sum_size / 1048576, 2)

    def __single_or_plural_grammar(self, count, single_statement, plural_statement):
        return single_statement if count == 1 else plural_statement

    def __candidate_file_count(self):
        return self.gateway.count()

    def __duplicate_file_count(self):
        return self.gateway.duplicate_count()

    def __name_clash_file_count(self):
        return self.gateway.name_clash_count()

    def __files_to_be_copied_size_sum(self):
        return sum(size for size in (self.gateway.sum_size_of_media_files_to_be_copied(),
                                     self.gateway.sum_size_of_misc_files_to_be_copied()) if size is not None)
