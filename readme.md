# Transfer Wizard
#### A tool to organise your media files by date into folders structured by year and quarter

##### Development notes:

This project is a work in progress and is under active development. As such use it at your own risk.

My main language is Ruby. I wanted to learn Python so that's the language I chose for this project. As such my coding style may be less Pythonic and more influenced by Ruby conventions.

I wanted to learn by experimenting, so some design decisions are unorthodox. e.g.: instead of using the built in logger I have built my own using the singleton pattern. The database controller also uses the singleton pattern.

I aim to use the Python standard library or build my own helpers and tools wherever possible. As such pytest and pytest-mock are the only external requirements.

### Overview

This program will allow you to unify your disparate photo and video libraries in to an organised directory structure.

It scans files in the source directory, analyses them, and copies them to the new directory structure in the destination directory.

Files are organised by year and quarter based on the approximate (see note on copy behaviour on different file systems, below) creation date of the files: 
```bash
└── destination_directory
    └── 2024
        └── Q1
            └── video.mov
        └── Q2
            └── pic.jpeg        
        └── Q3
            └── film.mkv        
        └── Q4
            └── cat.hevc
```

The program handles files with the same name but different sizes (name clash files) by copying the file and adding a unique suffix to the filename.

Duplicate files (files that have the same name and the same size) are identified and not copied.

The program gives a summary of files to be copied before asking for user confirmation of copy:

```commandline
Source directory: /source
Destination directory: /destination

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

`python main.py -s <your source directory> -t <your destination directory>`

You will be presented with statistics on the files you want to copy. You can then confirm the copy or cancel it.


### Current functionality
- Copies photos and videos from source directory to generated directory structure in destination directory
- Status update before copy
- Command line interface
- Has alternate mode where it lists file extensions that won't be copied from source directory
- Detailed log files

### Future functionality
- Reorganise (move) files in source directory instead of copying them to a new location.
- Pause and resume function
- Status updates during and after copy
- Scheduled backup functionality
- GUI

One day I plan to have a raspberry pi set up to detect my camera via bluetooth, copy all files from the camera to my cloud storage, and then delete the files on the camera. Progress will be displayed on a small screen on the raspberry pi. This will allow me to leave my camera turned on on my desk and walk away, with the media transfer happening automatically.

### Notes on copy behaviour of different file systems

On Windows the creation time (or birth time) is preserved when a file is copied. On Unix systems by default the creation time of a copied file is the time at which it was copied (for instance when copying with drag and drop). This program utilises the `shutil.copy2()` method, which wherever possible preserves the original file metadata when copying, even on Unix systems. This means that the program can be run twice on the same files and will be able to sort them again. 

I have designed this program to select the earlier of either the file birth time or modification time to be the date that is used to determine the destination directory. In future I may also check camera file metadata to determine the earliest date.

This is because I have some pictures on my Windows hard drive that somehow have a modified time that is before the creation time! I am unsure how this happened, but expect it happened during a transfer of some sort. The creation times are all the same, but the modified dates are different, leading me to believe that the modified dates are the dates that the photos were taken.