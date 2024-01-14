import argparse
import sys

from .helpers import clear_db_and_test_directories
from test.fixtures.main_fixtures import *
from main import main, PROGRAM_DESCRIPTION, ROOT_DIR, USAGE, _configure_parser


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def parse_args():
    return _configure_parser().parse_args(sys.argv[1:])


def test_parses_args_for_copying_media_files_only(set_copy_media_args):
    args = parse_args()
    assert args.source == source_directory
    assert args.destination == destination_root_directory


def test_parses_args_for_copying_all_filetypes(set_copy_all_filetypes_args):
    args = parse_args()
    assert args.source == source_directory
    assert args.destination == destination_root_directory
    assert args.miscellaneous is True


def test_parses_source_and_extension_path_args(set_source_and_ext_args):
    args = parse_args()
    assert args.source == source_directory
    assert args.extensions is True


def test_throws_error_and_provides_error_message_when_only_source_provided(capsys, set_only_source_arg):
    with pytest.raises(argparse.ArgumentError) as exc_info:
        main()

    assert 'Must provide source flag (-s <directory path>) and either ' \
           '-ext flag or -d flag (-d <directory path>)' in str(exc_info.value)


def test_throws_error_when_only_destination_provided(set_only_destination_arg):
    with pytest.raises(SystemExit):
        _configure_parser().parse_args(sys.argv[1:])


def test_throws_error_when_only_ext_provided(set_only_ext_arg):
    with pytest.raises(SystemExit):
        _configure_parser().parse_args(sys.argv[1:])


def test_throws_error_when_only_misc_provided(set_only_misc_arg):
    with pytest.raises(SystemExit):
        _configure_parser().parse_args(sys.argv[1:])


def test_throws_error_when_unexpected_arg_provided(set_unexpected_arg):
    with pytest.raises(SystemExit):
        _configure_parser().parse_args(sys.argv[1:])


def test_calls_expected_classes_when_source_and_extensions_args_provided(mocker, set_source_and_ext_args):
    mocked_directory_manager = mocker.patch('main.DirectoryManager')
    mocked_extension_presenter = mocker.patch('main.ExtensionPresenter')

    main()

    mocked_directory_manager.return_value.check_if_directory_exists.assert_called_once_with(source_directory)
    mocked_extension_presenter.assert_called_once_with(source_directory)
    mocked_extension_presenter.return_value.display_misc_extensions.assert_called_once()


def test_calls_expected_classes_when_source_and_destination_args_provided(mocker, set_copy_media_args):
    mocked_directory_manager = mocker.patch('main.DirectoryManager')
    mocked_copy_controller = mocker.patch('main.CopyController')

    main()

    mocked_directory_manager.return_value.check_if_directory_exists.assert_has_calls(
        [mocker.call(source_directory), mocker.call(destination_root_directory)], any_order=True)
    mocked_copy_controller.assert_called_once_with(destination_root_directory=destination_root_directory,
                                                   source_root_directory=source_directory,
                                                   include_misc_files=False)
    mocked_copy_controller.return_value.copy_files.assert_called_once()


def test_calls_expected_classes_when_source_and_destination_and_misc_args_provided(mocker, set_copy_all_filetypes_args):
    mocked_directory_manager = mocker.patch('main.DirectoryManager')
    mocked_copy_controller = mocker.patch('main.CopyController')

    main()

    mocked_directory_manager.return_value.check_if_directory_exists.assert_has_calls(
        [mocker.call(source_directory), mocker.call(destination_root_directory)], any_order=True)
    mocked_copy_controller.assert_called_once_with(destination_root_directory=destination_root_directory,
                                                   source_root_directory=source_directory,
                                                   include_misc_files=True)
    mocked_copy_controller.return_value.copy_files.assert_called_once()


def test_db_initializer_called_with_correct_args(mocker, set_copy_media_args):
    mocker.patch('main.DirectoryManager')
    mocker.patch('main.CopyController')
    mocked_db_initializer = mocker.patch('main.DBInitializer')

    main()

    mocked_db_initializer.assert_called_once_with(ROOT_DIR)


def test_program_description_text():
    assert _configure_parser().description == PROGRAM_DESCRIPTION


def test_program_usage_text():
    assert _configure_parser().usage == USAGE
