import shutil
import os


def copy_files(path, path_30, path_50):
    files = os.listdir(path)
    for file in files:
        if file.fond('_30_') != -1:
            shutil.copy(path+file, path_30+file)
        elif file.fond('_5_') != -1:
            shutil.copy(path+file, path_30+file)
        else:
            continue


