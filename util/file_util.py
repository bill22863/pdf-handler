# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:34:37 2022

@author: Bill
"""

from pathlib import Path
from PyPDF2 import PdfFileWriter
import log, logging
import os


file_logger = logging.getLogger(__name__)

class FileUtil:
    
    @staticmethod
    def get_path_str(p):
        return str(p)
    
    @staticmethod
    def get_file_list(dir_path):
        d = Path(dir_path)
        files = []
        # iterate dir
        for item in d.iterdir():
            if item.is_file():
                p = str(item.resolve())                
                files.append(p)
        return files        
    
    @staticmethod
    def get_path(root_path, *args):
        path = Path(root_path)
        # 取得新建資料夾路徑
        for p in args:
            # 斜線表示連接子路徑
            path = path / p
        
        #print(f"檔案路徑: {path}")
        msg = f"檔案路徑: {path}"
        #LogUtil.record(False, msg)        
        file_logger.info(msg)
        return path
    
    # 建立資料夾
    @staticmethod
    def create_dir(path):        
        try:    
            path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            #print(f"{path} 資料夾已建立")
            msg = f'錯誤: {path} 資料夾已存在'
            #LogUtil.record(True, msg)
            file_logger.error(msg)
       
        return None
    
    # 存檔
    @staticmethod
    def save_pdf(dest: str , writer: PdfFileWriter) -> None:
        with open(dest , 'wb') as out :
            writer.write(out)
        return None
    
    @staticmethod
    def delete(src: str) -> None:        
        try:
            os.remove(src)
            #print(f'Success: {src} 刪除成功')
            msg = f'{src} 檔案刪除成功'
            file_logger.info(msg)
            
        except OSError as e:
            #print(f'Error: {e.filename} - {e.strerror}')
            msg = f'錯誤: {e.filename} - {e.strerror}'
            file_logger.error(msg)
            
        return None