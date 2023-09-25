from app.file_gateway import FileGateway


class StatPresenter:

    def present_stats_to_user(self, source_directory, target_directory):  # TODO break this up and unit test it
        file_gateway = FileGateway()
        candidate_file_count = file_gateway.count()
        candidate_file_size_sum = file_gateway.sum_size()
        duplicate_file_count = file_gateway.duplicate_count()
        name_clash_file_count = file_gateway.name_clashes_count()
        to_be_copied_count = candidate_file_count - duplicate_file_count - name_clash_file_count
        files_to_be_copied_size_sum = file_gateway.sum_size_of_files_to_be_copied()
        print(f'Source directory: {source_directory}')
        print(f'Target directory: {target_directory}')
        print()
        print(f'{candidate_file_count} candidate photo and video files discovered in source directory.')
        print(f'Total size of candidate files: {self.__size_calc(candidate_file_size_sum)}MB')
        print()
        print(f'{duplicate_file_count} files are duplicates. Duplicates will not be copied.')
        print(f'{name_clash_file_count} files had name clashes. Files will be copied with a unique suffix.')
        print(f'{to_be_copied_count} files will be copied.')
        print()
        print(f'Total size of files to be copied: {self.__size_calc(files_to_be_copied_size_sum)}MB')
        print()

    def __size_calc(self, sum_size):
        if sum_size is None:
            return 0.0
        return round(sum_size / (1024 ** 2), 2)
