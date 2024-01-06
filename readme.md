# Transfer Wizard
#### A tool to organise your media files by date into folders structured by year and quarter

This project is a work in progress and is under active development. As such use it at your own risk.

Note: my main language is Ruby. I wanted to learn Python so that's the language I chose for this project. As such my coding style will not align with Pythonic conventions.

### Overview

This program will allow you to unify your disparate photo and video libraries in to an organised directory structure.

It scans files in the source directory, analyses them, and copies them to the new directory structure in the target directory.

Files are organised by year and quarter based on the creation date of the files: 
```bash
└── target_directory
    └── 2023
        └── Q1
            └── video.mov
        └── Q2
            └── pic.jpeg        
        └── Q3
            └── film.mkv        
        └── Q4
            └── cat.gif
```

The program handles files with the same name but different sizes (name clash files) by copying the file and adding a unique suffix to the filename.

Duplicate files (files that have the same name and the same size) are identified and not copied.

The program gives a summary of files to be copied before asking for user confirmation of copy:

```commandline
Source directory: /source
Destination directory: /target

7 candidate photo and video files discovered in source directory.
Total size of candidate files: 2.89MB

5 files are duplicates. Duplicates will not be copied.
0 files had name clashes. Files will be copied with a unique suffix.
2 files will be copied.

Total size of files to be copied: 0.63MB

Proceed with copy? ( y / n )
```

### Installation

The project is in beta; use at your own risk.

To run the project from the command line, navigate to the project root directory and run:

`python main.py -s <your source directory> -t <your target directory>`

You will be presented with statistics on the files you want to copy. You can then confirm the copy or cancel it.


### Current functionality
- Copies photos and videos from source directory to generated directory structure in target directory
- Status update before copy
- Command line interface
- Has alternate mode where it lists file extensions that won't be copied from source directory

### Future functionality
- Pause and resume function
- Status updates during and after copy
- Logging
- Scheduled backup functionality
- GUI
