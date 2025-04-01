from datetime import datetime
from exiftool import ExifToolHelper
from pathlib import Path
from PIL import Image, UnidentifiedImageError

from app.logger import Logger


class CaptureDateIdentifier:
    def media_capture_date(self, filepath):
        extension = ''
        try:
            extension = Path(filepath).suffix.lower()
            if extension == '.jpg':
                return self._pil_capture_date(filepath)
            if extension == '.raf' or extension == '.mov':
                return self._exiftool_capture_date(filepath)
            else:
                Logger().log_error('Extension not supported: ', SyntaxError, [filepath, extension])
                raise SyntaxError
        except (Exception, UnidentifiedImageError) as e:
            Logger().log_error('Media metadata read error: ', e, [filepath, extension])
            raise e

    def _pil_capture_date(self, photo_path):
        image = Image.open(photo_path)
        metadata = image.getexif().items()
        # noinspection PyTypeChecker
        capture_date_val = dict(metadata).get(306)
        capture_date = self._to_datetime(capture_date_val)
        return {'capture_date': capture_date, 'metadata_unreadable': False}

    def _exiftool_capture_date(self, video_path):
        media_creation_time_tag_name = 'EXIF:DateTimeOriginal'
        metadata = ExifToolHelper().get_metadata(video_path)[0]
        capture_date = self._to_datetime(metadata[media_creation_time_tag_name])
        return {'capture_date': capture_date, 'metadata_unreadable': False}

    def _to_datetime(self, original_capture_date):
        date_format = '%Y:%m:%d %H:%M:%S'
        return datetime.strptime(original_capture_date, date_format).date()
