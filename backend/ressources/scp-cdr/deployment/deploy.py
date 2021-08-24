#coding:utf-8

import os

def create_subfolder(cfg):
    folder,subfolders = [*cfg['deployement'].values()] 
    subfolder = subfolders.strip()
    subfolders = list(subfolder.split(','))
    calls = 'Calls'
    print(folder)
    if calls not in folder:
        os.mkdir(os.path.join(folder, calls))
    for sub in subfolders:
        if sub not in os.listdir(folder):
            if 'Calls' in sub:
                os.mkdir(os.path.join(folder+calls, sub.strip()))
            else:
                os.mkdir(os.path.join(folder, sub.strip()))
        else:
            continue

    for folder in os.listdir(folder):
        if folder not in subfolders:
            print(f"this folder{folder} was not created")
    return "All file was created!"
    

