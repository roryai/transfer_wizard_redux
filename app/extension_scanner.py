from app.directory_manager import DirectoryManager
from app.scanner import Scanner


class ExtensionScanner:

    def __init__(self, source_directory):
        DirectoryManager().check_if_directory_exists(source_directory)
        self.source_directory = source_directory

    def display_misc_extensions(self):
        extensions = Scanner().misc_extensions_in(self.source_directory)
        if len(extensions) == 0:
            print('No miscellaneous extensions found.')
        else:
            print('\nThe following miscellaneous file extensions are present in the source directory.\n'
                  'By default these files are not copied.\n'
                  'Consult the documentation to discover how to copy these files.')
            [print(ext.replace('.', '')) for ext in sorted(extensions)]
            print()
