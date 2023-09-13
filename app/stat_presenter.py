from app.file_gateway import FileGateway


class StatPresenter:

    def present_stats_to_user(self, source_directory, target_directory):
        file_gateway = FileGateway()
        count = file_gateway.count()
        sum_size = file_gateway.sum_size()
        duplicates = file_gateway.duplicate_count()
        name_clashes = file_gateway.name_clashes_count()
        print()
        print(f'{count} files selected to be transferred.')
        print(f'Total file size: {self.__size_calc(sum_size)}MB')
        print(f'{duplicates} files are duplicates. Duplicates will not be copied')
        print(f'{name_clashes} files had name clashes. Files will be copied with a unique suffix.')
        print(f'Source directory: {source_directory}')
        print(f'Target directory: {target_directory}')
        print()
        print(f'Proceed with transfer? ( y / n )')
        print()

    def __size_calc(self, sum_size):
        if sum_size is None:
            return 0.0
        return round(sum_size / (1024 ** 2), 3)
