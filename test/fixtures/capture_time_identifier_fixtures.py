import pytest

earlier = 987654321.0  # 19/04/01
later = 1234567890.0  # 13/02/09


@pytest.fixture
def birth_time_first(monkeypatch):
    monkeypatch.setattr('pathlib.Path.stat', lambda x: custom_stat_result)
    custom_stat_result = stat_result_mock(st_birthtime=earlier, st_mtime=later, st_ctime=later)

    return custom_stat_result


@pytest.fixture
def creation_time_first(monkeypatch):
    monkeypatch.setattr('pathlib.Path.stat', lambda x: custom_stat_result)
    custom_stat_result = stat_result_mock(st_birthtime=later, st_mtime=later, st_ctime=earlier)

    return custom_stat_result


@pytest.fixture
def modified_time_first(monkeypatch):
    monkeypatch.setattr('pathlib.Path.stat', lambda x: custom_stat_result)
    custom_stat_result = stat_result_mock(st_birthtime=later, st_mtime=earlier, st_ctime=later)

    return custom_stat_result


def stat_result_mock(st_birthtime, st_mtime, st_ctime):
    return type('StatResultMock', (), {'st_birthtime': st_birthtime,
                                       'st_mtime': st_mtime,
                                       'st_ctime': st_ctime})
