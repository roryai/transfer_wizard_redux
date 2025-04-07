import sys

from .helpers import cleanup
from test.fixtures.main_fixtures import *
from main import main, PROGRAM_DESCRIPTION, ROOT_DIR, USAGE, _configure_parser


@pytest.fixture(autouse=True)
def teardown():
    yield
    cleanup()


def parse_args():
    return _configure_parser().parse_args(sys.argv[1:])


def test_parses_args_for_copying_media_files(set_copy_media_args):
    args = parse_args()
    assert args.source == source_directory
    assert args.destination == destination_root_directory


def test_throws_error_when_only_source_provided(capsys, set_only_source_arg):
    with pytest.raises(SystemExit):
        _configure_parser().parse_args(sys.argv[1:])


def test_throws_error_when_only_destination_provided(set_only_destination_arg):
    with pytest.raises(SystemExit):
        _configure_parser().parse_args(sys.argv[1:])


def test_throws_error_when_unexpected_arg_provided(set_unexpected_arg):
    with pytest.raises(SystemExit):
        _configure_parser().parse_args(sys.argv[1:])


def test_calls_expected_classes_when_source_and_destination_args_provided(mocker, set_copy_media_args):
    mocked_directory_manager = mocker.patch('main.DirectoryManager')
    mocked_copy_controller = mocker.patch('main.CopyController')

    main()

    mocked_directory_manager.return_value.check_if_directory_exists.assert_has_calls(
        [mocker.call(source_directory), mocker.call(destination_root_directory)], any_order=True)
    mocked_copy_controller.assert_called_once_with(destination_root_directory, source_directory)
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
