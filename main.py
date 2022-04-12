# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:50:16 2022

@author: Bill
"""

from entity.db import DataBase

def main():
    database = DataBase()
    sponsors = database.query()
         


if __name__ == '__main__':
    main()