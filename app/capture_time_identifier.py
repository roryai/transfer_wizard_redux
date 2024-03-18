from datetime import datetime
from exiftool import ExifToolHelper
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from pillow_heif import register_heif_opener

from app.filetype_constants import extension_in_photo_filetypes, extension_in_video_filetypes
from app.logger import Logger


class CaptureTimeIdentifier:

    def __init__(self):
        register_heif_opener()

    def approximate_file_creation_date(self, filepath):
        try:
            extension = Path(filepath).suffix
            if extension_in_photo_filetypes(extension):
                return self._get_date_taken_for_photo(filepath)
            if extension_in_video_filetypes(extension):
                return self._get_date_taken_for_video(filepath)
            else:
                return self._earliest_file_system_date(filepath)
        except (IsADirectoryError, FileNotFoundError) as e:
            Logger().log_error('Attempting to approximate creation date', e, [filepath, extension])

    def _get_date_taken_for_photo(self, photo_path):
        metadata = {}
        try:
            image = Image.open(photo_path)
            metadata = image.getexif().items()
            # noinspection PyTypeChecker
            capture_date_string = dict(metadata).get(306)
            date_format = '%Y:%m:%d %H:%M:%S'
            capture_date = self._construct_datetime_object(capture_date_string, date_format)
            return {'capture_date': capture_date, 'metadata_unreadable': False}
        except (AttributeError, KeyError, IndexError, TypeError, UnidentifiedImageError) as e:
            context_message = 'Photo metadata read error, defaulting to file system date'
            Logger().log_error(context_message, e, [photo_path, str(metadata)])
            return self._earliest_file_system_date(photo_path, metadata_unreadable=True)

    def _get_date_taken_for_video(self, video_path):
        metadata = {}
        try:
            with ExifToolHelper() as et:
                metadata = et.get_metadata(video_path)[0]
                date_format, tag_name = self._determine_filetype_tag_info(metadata)
                capture_date = self._construct_datetime_object(metadata[tag_name], date_format)
                return {'capture_date': capture_date, 'metadata_unreadable': False}
        except (AttributeError, KeyError, IndexError, TypeError) as e:
            context_message = 'Video metadata read error, defaulting to file system date'
            Logger().log_error(context_message, e, [video_path, str(metadata)])
            return self._earliest_file_system_date(video_path, metadata_unreadable=True)

    def _earliest_file_system_date(self, filepath, metadata_unreadable=False):
        metadata = {}
        try:
            metadata = Path(filepath).stat()
            earliest_date = datetime.fromtimestamp(min(metadata.st_mtime,
                                                       metadata.st_birthtime,
                                                       metadata.st_ctime)).date()
            return {'capture_date': earliest_date, 'metadata_unreadable': metadata_unreadable}
        except (AttributeError, KeyError, IndexError) as e:
            Logger().log_error('Attempting to access file metadata', e, [filepath, metadata])

    def _construct_datetime_object(self, original_capture_time, date_format):
        if not original_capture_time:
            raise AttributeError('Not possible to read original capture time from metadata')
        return datetime.strptime(original_capture_time, date_format).date()

    def _determine_filetype_tag_info(self, metadata):
        date_format, tag_name = None, None
        for media_type in self._video_tag_info():
            if media_type['tag_name'] in metadata:
                tag_name = media_type['tag_name']
                date_format = media_type['date_format']
        if not date_format or not tag_name:
            raise AttributeError('Video metadata format not supported')
        return date_format, tag_name

    def _video_tag_info(self):
        quicktime = {'tag_name': 'QuickTime:CreateDate', 'date_format': '%Y:%m:%d %H:%M:%S'}
        h264 = {'tag_name': 'H264:DateTimeOriginal', 'date_format': '%Y:%m:%d %H:%M:%S%z'}
        riff = {'tag_name': 'RIFF:DateTimeOriginal', 'date_format': '%Y:%m:%d %H:%M:%S'}
        asf = {'tag_name': 'ASF:CreationDate', 'date_format': '%Y:%m:%d %H:%M:%SZ'}
        return [quicktime, h264, riff, asf]
