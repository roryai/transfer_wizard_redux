# Transfer Wizard
### A tool to organise your media files by date into folders structured by year and quarter

<img width="401" alt="Screenshot 2025-04-29 at 09 33 34" src="https://github.com/user-attachments/assets/6641aca9-6b94-407e-a42b-a0ef0ce5d685" />

I have used this program to confidently deduplicate and sort more than 45,000 photos and videos that I have taken over the course of more than 20 years.

My photos are my most treasured possession and it speaks to my thoroughness in writing and testing this program that I felt able to rely on it for such an important task.

I was able to point this program at several different hard drives that contained overlapping backups and copies of my photo library, and sort the photos to a single unified destination.

The [active branch](https://github.com/roryai/transfer_wizard_redux/tree/auto_xt4) is optimised for transferring photos from my Fuji X-T4. The plan is to have a script run the program to copy all photos from the camera to a NAS drive in my house each time the camera is connected.

### Overview

This program will allow you to unify your disparate photo and video libraries in to an organised directory structure.

It also allows you to copy photos from your camera to your hard drive .

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
        Discovered         To be copied       Duplicate          Name clash
        Count   Size       Count   Size       Count   Size       Count   Size
______________________________________________________________________________
Media   7       2.89MB     7       2.89MB     0       0.0MB      0       0.0MB      
Misc    0       0.0MB      0       0.0MB      0       0.0MB      0       0.0MB      
______________________________________________________________________________
Total   7       2.89MB     7       2.89MB     0       0.0MB      0       0.0MB      

Duplicates will not be copied
Name clash files will be copied with a unique suffix

Total to be copied:
7 files
2.89MB
```

##### Development notes:

This project is in beta and is under active development. See Roadmap section lower down for upcoming features and areas that need refactoring.

I aim to use the Python standard library or build my own helpers and tools wherever possible. As such pytest, pytest-mock, exiftool and pillow are the only dependencies.

There is only minimal error handling as I wanted errors to surface immediately during development and testing. Error handling is on the roadmap.

I prefer abbreviating lines for readability, so you (hopefully) won't see long lines going off the end of the screen.

My main language is Ruby. I wanted to learn Python and so taught myself whilst building this. As such I will not always follow Pythonic conventions.

I wanted to experiment with a few things so I've built my own logger and table generator. I have also explored using the singleton pattern.

Code reviews, feedback, and pull requests are welcome!

### Take a look at...
[FileCopier](https://github.com/roryai/transfer_wizard_redux/blob/main/app/file_copier.py) for recursion, and a guest appearance from the [controversial](https://pythonsimplified.com/the-most-controversial-python-walrus-operator) walrus operator!

[StatPresenter](https://github.com/roryai/transfer_wizard_redux/blob/main/app/stat_presenter.py) for some metaprogramming that was deeply satisfying to write. I love the result (see the pre-copy file summary table, below). I tried a couple of table generators, including pandas, but it was inadequate for what I wanted to do.

[Scanner](https://github.com/roryai/transfer_wizard_redux/blob/main/app/scanner.py) for clean design, and functions being passed to functions.

The [main.py tests](https://github.com/roryai/transfer_wizard_redux/blob/main/test/test_main.py) to see me pytest mocking and fixtures.


### Installation

The project is in beta; use at your own risk.

The fantastic [ExifTool](https://exiftool.org) is required to run this program, and needs to be in your PATH. Follow the instructions [here](https://pypi.org/project/PyExifTool/) to set it up.

To run the project from the command line, navigate to the project root directory and run:

`python main.py -s <your source directory> -t <your destination directory>`

You will be presented with statistics on the files you want to copy. You can then confirm the copy or cancel it.

### Roadmap

#### Current functionality
- Three modes
  - Copies photos and videos from source directory to generated directory structure in destination directory
  - Same as first mode, but copies the miscellaneous files to a single directory (/misc) in destination directory
  - Lists miscellaneous file extensions that won't be copied when above mode is run
- Detailed pre=copy summary of source file analysis
- Command line interface
- Detailed log files

#### Future functionality
- Reorganise (move vs copy) files in source directory instead of copying them to a destination directory.
- Pause and resume function
- Status updates during and after copy
- Scheduled backup functionality
- GUI
- Auto-runs when camera connected

#### Areas in need of refactoring
CaptureTimeIdentifier is a WIP and I am currently experiementing with two different libraries for extracting EXIF data for capture time. Exiftool works for videos and images but is relatively slow, and pillow only works for images. I haven't yet found a light weight library to extract capture time info from videos.
FileGateway is too large and needs splitting up.
Logger needs a rethink. Not sure I want to store so much in memory whilst the program is running.

One day I plan to have a raspberry pi set up to detect my camera via bluetooth, copy all files from the camera to my cloud storage, and then delete the files on the camera. Progress will be displayed on a small screen on the raspberry pi. This will allow me to leave my camera turned on on my desk and walk away, with the media transfer happening automatically.

### Notes on copy behaviour of different file systems

On Windows the creation time (or birth time) is preserved when a file is copied. On Unix systems by default the creation time of a copied file is the time at which it was copied (for instance when copying with drag and drop). This program utilises the `shutil.copy2()` method, which wherever possible preserves the original file metadata when copying, even on Unix systems. This means that the program can be run twice on the same files and will be able to sort them again. 

I have designed this program to select the earlier of either the file birth time, creation time, or modification time to be the date that is used to determine the destination directory. In future I may also check camera file metadata to determine the earliest date.

This is because I have some pictures on my Windows hard drive that somehow have a modified time that is before the creation time! I am unsure how this happened, but expect it happened during a transfer of some sort. The creation times are all the same, but the modified dates are different, leading me to believe that the modified dates are the dates that the photos were taken.
