import os
from datetime import datetime
import pathlib


class DirectoryGenerator:

    def generate_target_directory_path(self, source_filepath, target_directory):
        decimal_birthtime = os.stat(source_filepath).st_birthtime
        birthtime = datetime.fromtimestamp(decimal_birthtime)
        quarter = self.determine_quarter(birthtime.month)
        filename = pathlib.Path(source_filepath).name
        return f'{target_directory}{birthtime.year}/{quarter}/{filename}'

    def determine_quarter(self, month):
        match month:
            case 1 | 2 | 3:
                return 'Q1'
            case 4 | 5 | 6:
                return 'Q2'
            case 7 | 8 | 9:
                return 'Q3'
            case 10 | 11 | 12:
                return 'Q4'
            case _:
                raise TypeError
