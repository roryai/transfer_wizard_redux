from exiftool import ExifToolHelper


class ExiftoolWrapperMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(ExiftoolWrapperMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class ExiftoolWrapper(metaclass=ExiftoolWrapperMeta):

    def exiftool(self):
        return ExifToolHelper()
