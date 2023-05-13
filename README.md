# Folder-Sync

A Python script that synchronizes two given folders. One folder, called the **replica folder**, will be updated based on a **source folder** after a given number of minutes. The updates will be recorded both in the console and in a given file.

## How to Run:

Run the following command in a CLI:

*python FolderSync.py <source_path> <replica_path> <log_path> <sync_interval>*, where:

- **source_path** is the path to the source folder,
- **replica_path** is the path to the replica folder,
- **log_path** is the path to the log file,
- **sync_interval** is the time interval in **minutes** after which the script checks again for new changes in the source folder.

Two test folders, source and replica, are included in the repository for testing the script. A log file with a test run of the script is also included.

## Restrictions

- *log_path* must be a valid path (*source_path* and *replica_path* are checked for validity in the code);
- *sync_interval* must be an integer.
