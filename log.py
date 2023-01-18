# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:16:25 2023

@author: Bill
"""

from datetime import date
import logging
import os

prefix = date.today()
log_dir = r'D:/log/op_report'
log_name = f'{prefix}_report.log'

# log path
log_path = log_dir + '/' + log_name
os.makedirs(log_dir , exist_ok=True)

# create root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO) 

# create file handler
fileHandler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
# create formatter
formatter = logging.Formatter("%(asctime)s %(name)-5s: %(levelname)-8s %(message)s")
fileHandler.setFormatter(formatter)

# console handler
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('%(name)-5s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)

# root logger add handler
root_logger.addHandler(fileHandler)
root_logger.addHandler(console)

def close_log():
    handler_list = root_logger.handlers[:]
    for handler in handler_list:
        root_logger.removeHandler(handler)
        handler.close()