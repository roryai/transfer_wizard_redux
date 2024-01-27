from app.filetype_constants import MEDIA_FILETYPES


def test_media_extensions_includes_all_video_and_photo_extensions():
    media_exts = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic',
                  '.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc', '.mts', '.m2ts']
    assert sorted(MEDIA_FILETYPES) == sorted(media_exts)
