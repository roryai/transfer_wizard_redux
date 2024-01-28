from datetime import datetime
from pathlib import Path

from app.exiftool_wrapper import ExiftoolWrapper
from app.filetype_constants import extension_in_photo_filetypes, extension_in_video_filetypes
from app.logger import Logger


class CaptureTimeIdentifier:

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
            Logger().log_error('Attempting to approximate creation date', e, filepath)

    def _get_date_taken_for_photo(self, photo_path):
        try:
            metadata = self._get_metadata(photo_path)
            original_capture_time = metadata['EXIF:DateTimeOriginal']
            date_format = '%Y:%m:%d %H:%M:%S'
            return self._construct_datetime_object(date_format, original_capture_time)
        except (AttributeError, KeyError, IndexError) as e:
            context_message = 'Photo metadata read error, defaulting to file system date'
            Logger().log_error(context_message, e, metadata)
            return self._earliest_file_system_date(photo_path)

    def _get_date_taken_for_video(self, video_path):
        try:
            metadata = self._get_metadata(video_path)
            date_format, tag_name = self._determine_filetype_tag_info(metadata)
            original_capture_time = metadata[tag_name]
            return self._construct_datetime_object(date_format, original_capture_time)
        except (AttributeError, KeyError, IndexError) as e:
            context_message = 'Video metadata read error, defaulting to file system date'
            Logger().log_error(context_message, e, metadata)
            return self._earliest_file_system_date(video_path)

    def _earliest_file_system_date(self, filepath):
        try:
            file_metadata = Path(filepath).stat()
            return datetime.fromtimestamp(min(file_metadata.st_mtime,
                                              file_metadata.st_birthtime,
                                              file_metadata.st_ctime)).date()
        except (AttributeError, KeyError, IndexError) as e:
            Logger().log_error('Attempting to access file metadata', e, metadata)

    def _get_metadata(self, filepath):
        return ExiftoolWrapper().exiftool().get_metadata(filepath)[0]

    def _construct_datetime_object(self, date_format, original_capture_time):
        return datetime.strptime(original_capture_time, date_format).date()

    def _determine_filetype_tag_info(self, metadata):
        for media_type in self._video_tag_info():
            if media_type['tag_name'] in metadata:
                tag_name = media_type['tag_name']
                date_format = media_type['date_format']
        return date_format, tag_name

    def _video_tag_info(self):
        quicktime = {'tag_name': 'QuickTime:CreateDate', 'date_format': '%Y:%m:%d %H:%M:%S'}
        h264 = {'tag_name': 'H264:DateTimeOriginal', 'date_format': '%Y:%m:%d %H:%M:%S%z'}
        riff = {'tag_name': 'RIFF:DateTimeOriginal', 'date_format': '%Y:%m:%d %H:%M:%S'}
        asf = {'tag_name': 'ASF:CreationDate', 'date_format': '%Y:%m:%d %H:%M:%SZ'}
        return [quicktime, h264, riff, asf]
