import os
import re
import shutil
import filecmp
import time


def log_message(log_path, msg):
    print(msg)
    with open(log_path, 'a') as log:
        log.write(msg)


def folder_sync_recursive(source_path, replica_path, log_path):
    dir_list_replica = os.listdir(replica_path)
    # Examples of strings the regular expression for folder_list matches:
    # "a", ".b" etc.
    # Examples of strings the regular expression for file_list matches:
    # "file.txt", ".file2.docx" etc.
    folder_list_replica = [f for f in dir_list_replica if re.fullmatch("\\.?\\w+", f)]
    file_list_replica = [f for f in dir_list_replica if re.fullmatch("\\.?\\w+\\.\\w+", f)]
    # Check if the source folder exists (if not, the replica folder will be deleted)
    if not os.path.exists(source_path):
        # Delete the folders in the replica folder recursively
        for folder in folder_list_replica:
            folder_sync_recursive(os.path.join(source_path, folder), os.path.join(replica_path, folder), log_path)
            os.rmdir(os.path.join(replica_path, folder))
            msg = "The folder " + os.path.join(replica_path, folder) + " has been deleted.\n"
            log_message(log_path, msg)
        # Delete the files in the replica folder
        for file in file_list_replica:
            os.remove(os.path.join(replica_path, file))
            msg = "The file " + os.path.join(replica_path, file) + " has been deleted.\n"
            log_message(log_path, msg)
        # The replica folder itself will be deleted in the parent call (or later in the function, if it is
        # the folder that first accessed this if clause)
        return
    dir_list_source = os.listdir(source_path)
    folder_list_source = [f for f in dir_list_source if re.fullmatch("\\.?\\w+", f)]
    file_list_source = [f for f in dir_list_source if re.fullmatch("\\.?\\w+\\.\\w+", f)]
    # Create all the newly added folders in the source folder inside the replica folder
    for folder in folder_list_source:
        if folder not in folder_list_replica:
            os.mkdir(os.path.join(replica_path, folder))
            msg = "The folder " + os.path.join(replica_path, folder) + " has been created.\n"
            log_message(log_path, msg)
    dir_list_replica = os.listdir(replica_path)
    folder_list_replica = [f for f in dir_list_replica if re.fullmatch("\\.?\\w+", f)]
    file_list_replica = [f for f in dir_list_replica if re.fullmatch("\\.?\\w+\\.\\w+", f)]
    # Access all the folders in the replica folder recursively
    for folder in folder_list_replica:
        folder_sync_recursive(os.path.join(source_path, folder), os.path.join(replica_path, folder), log_path)
        # Check if the current folder has to be deleted (the recursive call above already prepared the
        # folder for deletion)
        if folder not in folder_list_source:
            os.rmdir(os.path.join(replica_path, folder))
            msg = "The folder " + os.path.join(replica_path, folder) + " has been deleted.\n"
            log_message(log_path, msg)
    for file in file_list_source:
        # Create the newly added files in the source folder inside the replica folder
        if file not in file_list_replica:
            shutil.copyfile(os.path.join(source_path, file), os.path.join(replica_path, file))
            msg = "The file " + os.path.join(replica_path, file) + " has been created.\n"
            log_message(log_path, msg)
        else:
            # Update the existing files if they are different from the files in the source folder
            # The shallow=False argument ensures that the two files will be compared by checking their contents
            if not filecmp.cmp(os.path.join(source_path, file), os.path.join(replica_path, file), shallow=False):
                shutil.copyfile(os.path.join(source_path, file), os.path.join(replica_path, file))
                msg = "The file " + os.path.join(replica_path, file) + " has been updated.\n"
                log_message(log_path, msg)
    dir_list_replica = os.listdir(replica_path)
    file_list_replica = [f for f in dir_list_replica if re.fullmatch("\\.?\\w+\\.\\w+", f)]
    # Delete all the files in the replica folder that no longer exist in the source folder
    for file in file_list_replica:
        if file not in file_list_source:
            os.remove(os.path.join(replica_path, file))
            msg = "The file " + os.path.join(replica_path, file) + " has been deleted.\n"
            log_message(log_path, msg)


# folder_sync assumes (and therefore does not check) that log_path is valid
def folder_sync(source_path, replica_path, log_path, sync_interval):
    # Check that both of the paths given are valid, otherwise the program will exit automatically
    if not os.path.exists(source_path) or not os.path.exists(replica_path):
        print("At least one of the folder paths given is invalid!")
        return
    while True:
        log_message(log_path, "The synchronization started:\n")
        folder_sync_recursive(source_path, replica_path, log_path)
        log_message(log_path, "The synchronization has successfully completed.\n")
        # sync_interval is expressed in minutes and must be converted in seconds when calling time.sleep
        time.sleep(60 * int(sync_interval))


if __name__ == '__main__':
    import sys
    folder_sync(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
