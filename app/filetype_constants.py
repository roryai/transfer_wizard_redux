PHOTO_FILETYPES = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic']
VIDEO_FILETYPES = ['.mp4', '.mov', '.avi', '.wmv', '.mkv', '.hevc', '.mts']
MEDIA_FILETYPES = [ext.upper() for extensions in [PHOTO_FILETYPES, VIDEO_FILETYPES] for ext in extensions] \
                  + PHOTO_FILETYPES + VIDEO_FILETYPES