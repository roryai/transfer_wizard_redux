import pytest

earlier = 987654321.0  # 19/04/01
later = 1234567890.0  # 13/02/09


@pytest.fixture
def birthtime_earlier(monkeypatch):
    monkeypatch.setattr("pathlib.Path.stat", lambda x: custom_stat_result)
    custom_stat_result = stat_result_mock(st_birthtime=earlier, st_mtime=later)

    return custom_stat_result


def stat_result_mock(st_birthtime, st_mtime):
    return type("StatResultMock", (), {"st_birthtime": st_birthtime, "st_mtime": st_mtime})


@pytest.fixture
def birthtime_later(monkeypatch):
    monkeypatch.setattr("pathlib.Path.stat", lambda x: custom_stat_result)
    custom_stat_result = stat_result_mock(st_birthtime=later, st_mtime=earlier)

    return custom_stat_result
