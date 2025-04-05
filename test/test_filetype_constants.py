from app.filetype_constants import *


def test_media_extensions_includes_all_video_and_photo_extensions():
    media_exts = ['.jpg', '.mov', '.raf']
    assert sorted(MEDIA_FILETYPES) == sorted(media_exts)


def test_determines_if_jpg_extension_is_in_photo_filetypes():
    assert extension_in_photo_filetypes('.jpg') is True


def test_determines_if_mov_extension_is_in_video_filetypes():
    assert extension_in_video_filetypes('.mov') is True


def test_determines_if_raf_extension_is_in_photo_filetypes():
    assert extension_in_photo_filetypes('.raf') is True


def test_determines_if_media_extensions_are_in_media_filetypes():
    assert extension_in_media_filetypes('.raf') is True
    assert extension_in_media_filetypes('.jpg') is True
    assert extension_in_media_filetypes('.mov') is True
