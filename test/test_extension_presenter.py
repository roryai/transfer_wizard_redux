from app.extension_presenter import ExtensionPresenter
from .helpers import pytest, create_file_on_disk_with_data, clear_db_and_test_directories, source_directory


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def display_misc_extensions():
    ExtensionPresenter(source_directory).display_misc_extensions()


def test_displays_misc_extension_information_when_misc_extensions_are_present(capsys):
    create_file_on_disk_with_data(source_directory, 'filename.non')
    create_file_on_disk_with_data(source_directory, 'filename.err')

    display_misc_extensions()

    result = capsys.readouterr().out
    expected = """
The following miscellaneous file extensions are present in the source directory.
By default these files are not copied.
Consult the documentation to discover how to copy these files.

err
non

"""

    assert result == expected


def test_displays_message_when_no_misc_extensions_are_present(capsys):
    display_misc_extensions()

    result = capsys.readouterr().out
    expected = 'No miscellaneous extensions found.\n'

    assert result == expected
