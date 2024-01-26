from datetime import datetime

import exiftool


class CaptureTimeIdentifier:

    def get_date_taken_for_photo(self, photo_path):
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(photo_path)[0]
            original_capture_time = metadata['EXIF:DateTimeOriginal']
        date_format = '%Y:%m:%d %H:%M:%S'
        return datetime.strptime(original_capture_time, date_format).date()

    def get_date_taken_for_video(self, video_path):
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(video_path)[0]
            date_format, tag_name = self._determine_filetype_tag_info(metadata)
            original_capture_time = metadata[tag_name]
            return datetime.strptime(original_capture_time, date_format).date()

    def _determine_filetype_tag_info(self, metadata):
        for media_type in self._video_tag_info():
            if media_type['tag_name'] in metadata:
                tag_name = media_type['tag_name']
                date_format = media_type['date_format']
        return date_format, tag_name

    def _video_tag_info(self):
        h264 = {'tag_name': 'H264:DateTimeOriginal', 'date_format': '%Y:%m:%d %H:%M:%S%z'}
        quicktime = {'tag_name': 'QuickTime:CreateDate', 'date_format': '%Y:%m:%d %H:%M:%S'}
        return [h264, quicktime]
