# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:34:37 2022

@author: Bill
"""

from pathlib import Path
from PyPDF2 import PdfFileWriter, PdfFileReader

class FileUtil:
    
    @staticmethod
    def get_path_str(p):
        return str(p)
    
    @staticmethod
    def get_path(root_path, *args):
        path = Path(root_path)
        # 新建資料夾路徑
        for p in args:
            path = path / p
        
        print(f"file path: {path}")
        return path
    
    # 建立資料夾
    @staticmethod
    def create_dir(path):        
        try:    
            path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            print("Folder is already there")
        else:
            print("Folder was created")
        return path
    
    # 存檔
    @staticmethod
    def save_pdf(dest: str , writer: PdfFileWriter) -> None:
        with open(dest , 'wb') as out :
            writer.write(out)
        return None