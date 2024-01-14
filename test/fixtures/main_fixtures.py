import pytest

source_directory = '/source_directory'
destination_directory = '/destination_directory'


@pytest.fixture
def set_default_copy_args(monkeypatch):
    set_args(monkeypatch, ['-s', source_directory, '-d', destination_directory])


@pytest.fixture
def set_source_and_ext_args(monkeypatch):
    set_args(monkeypatch, ['-s', source_directory, '-ext'])


@pytest.fixture
def set_only_source_arg(monkeypatch):
    set_args(monkeypatch, ['-s', source_directory])


@pytest.fixture
def set_only_destination_arg(monkeypatch):
    set_args(monkeypatch, ['-d', destination_directory])


@pytest.fixture
def set_only_ext_arg(monkeypatch):
    set_args(monkeypatch, ['-ext'])


@pytest.fixture
def set_unexpected_arg(monkeypatch):
    set_args(monkeypatch, ['-unexpected'])


def set_args(monkeypatch, args):
    monkeypatch.setattr('sys.argv', ['main.py', *args])
