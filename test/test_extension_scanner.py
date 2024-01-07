from app.extension_scanner import ExtensionScanner
from .helpers import *


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_test_directories()


def display_invalid_extensions():
    ExtensionScanner(source_directory).display_invalid_extensions()


def test_displays_invalid_extension_information_when_invalid_extensions_are_present(capsys):
    create_file_with_data(source_directory, 'filename.non')
    create_file_with_data(source_directory, 'filename.err')

    display_invalid_extensions()

    result = capsys.readouterr().out
    expected = """
The following file extensions are present in the source directory.
Files with these extensions are invalid and will not be copied.
err
non

"""

    assert result == expected


def test_displays_invalid_extension_information_when_no_invalid_extensions_are_present(capsys):
    display_invalid_extensions()

    result = capsys.readouterr().out
    expected = 'No invalid extensions found.\n'

    assert result == expected
