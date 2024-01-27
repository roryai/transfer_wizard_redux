PHOTO_FILETYPES = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic']
VIDEO_FILETYPES = ['.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc', '.mts', '.m2ts']
MEDIA_FILETYPES = PHOTO_FILETYPES + VIDEO_FILETYPES


def extension_in_photo_filetypes(extension):
    return _extension_in(extension, PHOTO_FILETYPES)


def extension_in_video_filetypes(extension):
    return _extension_in(extension, VIDEO_FILETYPES)


def extension_in_media_filetypes(extension):
    return _extension_in(extension, MEDIA_FILETYPES)


def extension_not_in_media_filetypes(extension):
    return extension.lower() not in MEDIA_FILETYPES


def _extension_in(extension, filetypes):
    return extension.lower() in filetypes
