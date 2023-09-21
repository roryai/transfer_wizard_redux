# Media File Organiser
#### A tool to organise your media files and folders

### Overview

The aim of this project is to point the program at folders of unorganised photos and sort them in to folders organised by year and quarter (Q1 - Q4).

Files with name clashes are sorted in to a separate folder for you to check through manually. Once you have deleted undesired files then you can point the program at this folder to sort them in to the organised directory structure.

I made this because I have many different photo libraries and phone backups across several hard drives that contain partially duplicated photo sets and wanted to unify them in an organised structure.

### Installation

The project is a work in progress and is not currently ready for use.

### Current functionality
- Identifies all desired media files by file extension
- Generates a target file path including the year and quarter
- Name clashes are handled by adding a suffix to the filename
- Files are copied to the target directory
- Command line interface

Duplicated files are defined as having an existing file in the target directory with the same name and size as the source file. These files are skipped.

Name clash files have the same name but are of different sizes. These files are copied with new filenames.

### Future functionality
- SQL to enable:
  1. Filtering duplicates at the database level
  2. Pause and resume function
- Status updates before, during and after copy
- Logging
- Scheduled backup functionality- e.g. a daily backup of any new photos that have been added to your hard drive.
- GUI