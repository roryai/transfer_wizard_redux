import argparse

from .helpers import pytest, clear_db_and_test_directories
from main import main, parse_args, ROOT_DIR


@pytest.fixture(autouse=True)
def teardown():
    yield
    clear_db_and_test_directories()


def test_parses_source_and_destination_path_args():
    args_list = ['-s', '/copy_test_source', '-d', '/copy_test_dest']
    args = parse_args(args_list)

    assert args.source == '/copy_test_source'
    assert args.destination == '/copy_test_dest'


def test_parses_source_and_extension_path_args():
    args_list = ['-s', '/copy_test_source', '-ext']
    args = parse_args(args_list)

    assert args.source == '/copy_test_source'
    assert args.extensions is True


def test_throws_error_and_provides_error_message_when_only_source_provided(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['main.py', '-s', '/source_directory'])
    with pytest.raises(argparse.ArgumentError) as exc_info:
        main()

    assert 'Must provide source flag (-s <directory path>) and either ' \
           '-ext flag or -d flag (-d <directory path>)' in str(exc_info.value)


def test_throws_error_when_only_destination_provided():
    with pytest.raises(SystemExit):
        args_list = ['-d', '/copy_test_dest']
        parse_args(args_list)


def test_throws_error_when_only_ext_provided():
    with pytest.raises(SystemExit):
        args_list = ['-ext']
        parse_args(args_list)


def test_throws_error_when_unexpected_arg_provided():
    with pytest.raises(SystemExit):
        args_list = ['-random']
        parse_args(args_list)


def test_calls_expected_classes_when_source_and_extensions_args_provided(mocker, monkeypatch):
    mocked_directory_manager = mocker.patch('main.DirectoryManager')
    mocked_extension_scanner = mocker.patch('main.ExtensionScanner')
    source_dir = '/source_directory'
    monkeypatch.setattr('sys.argv', ['main.py', '-s', source_dir, '-ext'])

    main()

    mocked_directory_manager.return_value.check_if_directory_exists.assert_called_once_with(source_dir)
    mocked_extension_scanner.assert_called_once_with(source_dir)
    mocked_extension_scanner.return_value.display_misc_extensions.assert_called_once()


def test_calls_expected_classes_when_source_and_destination_args_provided(mocker, monkeypatch):
    mocked_directory_manager = mocker.patch('main.DirectoryManager')
    mocked_copy_controller = mocker.patch('main.CopyController')
    source_dir = '/source_directory'
    destination_dir = '/destination_directory'
    monkeypatch.setattr('sys.argv', ['main.py', '-s', source_dir, '-d', destination_dir])

    main()

    mocked_directory_manager.return_value.check_if_directory_exists.assert_has_calls(
        [mocker.call(source_dir), mocker.call(destination_dir)], any_order=True)
    mocked_copy_controller.assert_called_once_with(destination_root_directory=destination_dir,
                                                   source_root_directory=source_dir)
    mocked_copy_controller.return_value.copy_media_files.assert_called_once()


def test_db_initializer_called_with_correct_args(mocker, monkeypatch):
    monkeypatch.setattr('sys.argv', ['main.py', '-s', '/source_dir', '-d', '/destination_dir'])
    mocker.patch('main.DirectoryManager')
    mocker.patch('main.CopyController')
    mocked_db_initializer = mocker.patch('main.DBInitializer')

    main()

    mocked_db_initializer.assert_called_once_with(ROOT_DIR)
