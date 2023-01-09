# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:37:34 2023

@author: Bill
"""
from datetime import date
import logging
import os

class LogUtil:
    
    # private variable add single underline.
    _log_prefix = date.today()
    _log_name = f'{_log_prefix}_report.log'
    
    _log_dir = r'D:/log/op_report'
    
    # log path
    _log_path = _log_dir + '/' + _log_name
    os.makedirs(_log_dir, exist_ok=True)    
    
    # create logger and set level
    logger = logging.getLogger('pdfLogger')
    logger.setLevel(logging.INFO)
    
    # create file handler
    fileHandler = logging.FileHandler(_log_path, mode='w' , encoding='utf-8')
    fileHandler.setLevel(logging.INFO)
        
    # create formatter
    _formatter = logging.Formatter("%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s: %(message)s")
    fileHandler.setFormatter(_formatter)
    
    # logger add handler 
    logger.addHandler(fileHandler)
    
    @classmethod
    def record(cls, is_err , msg):
        if is_err:            
            cls.logger.error(msg)
        else:
            cls.logger.info(msg)
            
            
    