from datetime import datetime
from exiftool import ExifToolHelper
from pathlib import Path
from PIL import Image, UnidentifiedImageError

from app.logger import Logger


class CaptureDateIdentifier:
    def capture_date(self, filepath):
        extension = ''
        try:
            extension = Path(filepath).suffix.lower()
            if extension == '.jpg':
                return self._pil_capture_date(filepath)
            if extension == '.raf' or extension == '.mov':
                return self._exiftool_capture_date(filepath)
            else:
                Logger().log_error('Extension not supported: ', SyntaxError, [filepath, extension])
                Logger().finalise_logging()
                raise SyntaxError
        except (Exception, UnidentifiedImageError) as e:
            Logger().log_error('Metadata read error: ', e, [filepath, extension])
            Logger().finalise_logging()
            raise e

    def _pil_capture_date(self, photo_path):
        image = Image.open(photo_path)
        metadata = image.getexif().items()
        # noinspection PyTypeChecker
        capture_date_val = dict(metadata).get(306)
        return self._to_datetime(capture_date_val)

    def _exiftool_capture_date(self, video_path):
        creation_time_tag_name = 'EXIF:DateTimeOriginal'
        metadata = ExifToolHelper().get_metadata(video_path)[0]
        return self._to_datetime(metadata[creation_time_tag_name])

    def _to_datetime(self, original_capture_date):
        date_format = '%Y:%m:%d %H:%M:%S'
        return datetime.strptime(original_capture_date, date_format).date()
