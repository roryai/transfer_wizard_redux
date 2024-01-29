class ModeFlagsMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(ModeFlagsMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class ModeFlags(metaclass=ModeFlagsMeta):

    def __init__(self, year_mode=False):
        self.year_mode = year_mode
