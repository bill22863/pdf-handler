# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:43:21 2022

@author: Bill
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd

try:
    connection_config_dict = {
        'user': 'ctc_contract',
        'password': 'CTC@contract@6023',
        'host': 'localhost',
        'database': 'contractmanagement',
        'port': 3310
    }
    
    connection = mysql.connector.connect(**connection_config_dict)
    if connection.is_connected():
        #db query
        query = " select sc.IRB_No, b.Info_Name_Ch as spon from ( " \
        " select IRB_No, Manu_Name from signed_contract where Is_DC= 'N' " \
        " and Is_Intrust = 'Y' and Is_Required_Rpt = 'Y' and Execute_Id <> '0014') sc " \
        " left join " \
        " ( select Info_Id, Info_Name_Ch from basic_info where Info_Type = 'spon' and " \
        " (Info_Name_Ch like '%默沙東%' or Info_Name_Ch like '%AstraZeneca%' " \
        " or Info_Name_Ch like '%阿斯特捷利康%') ) as b on sc.Manu_Name = b.Info_Id " \
        
        df = pd.read_sql(query, connection);
        print("query finish.")
        
except Error as e:
    print("Error while connecting to MySQL", e)
    
finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL connection is closed")