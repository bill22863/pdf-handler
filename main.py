# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:50:16 2022

@author: Bill
"""

from entity.db import DataBase

file_path = 'src/11102-受試者編號2.xls'
dest = 'src/測試.xlsx'


def main():
    database = DataBase()
    sponsors = database.query()
         


if __name__ == '__main__':
    main()
    