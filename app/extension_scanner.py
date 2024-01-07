from app.directory_manager import DirectoryManager
from app.scanner import Scanner


class ExtensionScanner:

    def __init__(self, source_directory):
        DirectoryManager().check_if_directory_exists(source_directory)
        self.source_directory = source_directory

    def display_invalid_extensions(self):
        extensions = Scanner().invalid_extensions_in(self.source_directory)
        if len(extensions) == 0:
            print('No invalid extensions found.')
        else:
            print('\nThe following file extensions are present in the source directory.\n'
                  'Files with these extensions are invalid and will not be copied.')
            [print(ext.replace('.', '')) for ext in sorted(extensions)]
            print()
