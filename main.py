from pathlib import Path
from app.scanner import Scanner
from app.transfer import Transfer


def main():
    cwd = str(Path(__file__).parent)
    source_directory = cwd + '/test/media/static_source/'
    target_directory = cwd + '/test/media/target/'
    filepaths = Scanner().scan_dirs(source_directory)
    Transfer().copy_files(filepaths, target_directory)


if __name__ == '__main__':
    main()
