PHOTO_FILETYPES = ['.jpg', '.raf']
VIDEO_FILETYPES = ['.mov']
MEDIA_FILETYPES = PHOTO_FILETYPES + VIDEO_FILETYPES


def extension_in_photo_filetypes(extension):
    return _extension_in(extension, PHOTO_FILETYPES)


def extension_in_video_filetypes(extension):
    return _extension_in(extension, VIDEO_FILETYPES)


def extension_in_media_filetypes(extension):
    return _extension_in(extension, MEDIA_FILETYPES)


def _extension_in(extension, filetypes):
    return extension.lower() in filetypes
