from app.filetype_constants import *


def test_media_extensions_includes_all_video_and_photo_extensions():
    media_exts = ['.jpg', '.jpeg', '.tif', '.tiff', '.heic',
                  '.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc', '.mts', '.m2ts']
    assert sorted(MEDIA_FILETYPES) == sorted(media_exts)


def test_determines_if_photo_extension_is_in_photo_filetypes():
    assert extension_in_photo_filetypes('.heic') is True


def test_determines_if_video_extension_is_in_video_filetypes():
    assert extension_in_video_filetypes('.mp4') is True


def test_determines_if_media_extensions_are_in_media_filetypes():
    assert extension_in_media_filetypes('.wmv') is True
    assert extension_in_media_filetypes('.avi') is True


def test_determines_if_misc_extension_is_not_in_media_filetypes():
    assert extension_not_in_media_filetypes('.txt') is True


def test_determines_if_media_extensions_are_not_in_media_filetypes():
    assert extension_not_in_media_filetypes('.hevc') is False
    assert extension_not_in_media_filetypes('.avi') is False


def test_determines_if_misc_extension_is_in_photo_filetypes():
    assert extension_in_photo_filetypes('.txt') is False


def test_determines_if_misc_extension_is_in_video_filetypes():
    assert extension_in_video_filetypes('.txt') is False


def test_determines_if_video_extension_is_in_photo_filetypes():
    assert extension_in_photo_filetypes('.wmv') is False


def test_determines_if_photo_extension_is_in_video_filetypes():
    assert extension_in_video_filetypes('.jpeg') is False
