from app.filetype_constants import MEDIA_FILETYPES


def test_media_extensions_includes_upper_and_lower_case_extensions():
    media_exts = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic',
                  '.BMP', '.JPG', '.JPEG', '.PNG', '.TIF', '.TIFF', '.HEIC',
                  '.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc', '.mts',
                  '.MP4', '.MOV', '.AVI', '.WMV', '.MKV', '.HEVC', '.MTS']
    assert sorted(MEDIA_FILETYPES) == sorted(media_exts)
