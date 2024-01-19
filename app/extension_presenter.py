from app.directory_manager import DirectoryManager
from app.scanner import Scanner


class ExtensionPresenter:

    def __init__(self, source_directory):
        DirectoryManager().check_if_directory_exists(source_directory)
        self.source_directory = source_directory
        self.no_exts_found_message = 'No miscellaneous extensions found.'
        self.exts_found_message = """
The following miscellaneous file extensions are present in the source directory.
By default these files are not copied.
Consult the documentation to discover how to copy these files.
"""

    def display_misc_extensions(self):
        extensions = Scanner().misc_extensions_in(self.source_directory)
        if not extensions:
            print(self.no_exts_found_message)
        else:
            print(self.exts_found_message)
            self._print_extensions_without_periods(extensions)

    def _print_extensions_without_periods(self, extensions):
        [print(ext.replace('.', '')) for ext in sorted(extensions)]
        print()
