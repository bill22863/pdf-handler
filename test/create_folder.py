# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 16:50:39 2022

@author: Bill
"""
from pathlib import Path

network_drive_path=r"\\172.19.61.159\月報表明細"
sub_dir = "歷年資料二"

def create_dir():

    path = Path(network_drive_path) / sub_dir
    try:    
        path.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        print("Folder is already there")
    else:
        print("Folder was created")
        


if __name__ == '__main__':
    create_dir()