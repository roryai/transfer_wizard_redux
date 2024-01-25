from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS


class CaptureTimeIdentifier:

    def get_date_taken(self, photo_path):
        try:
            image = Image.open(photo_path)
            exif_data = image.getexif().items()
            # noinspection PyTypeChecker
            original_capture_time = dict(exif_data).get(306)
            date_format = '%Y:%m:%d %H:%M:%S'
            return datetime.strptime(original_capture_time, date_format).date()

        except (AttributeError, KeyError, IndexError):
            # Handle cases where there is no EXIF data or other issues
            return None


