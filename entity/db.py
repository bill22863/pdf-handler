# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:43:21 2022

@author: Bill
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd


class DataBase:
    # 連線資訊
    connection_config_dict = {
        'user': 'user',
        'password': '9N00@4003',
        'host': '172.19.61.158',
        'database': 'contractmanagement',
        'port': 3310
    }
    
    sql = " select sc.IRB_No, b.Info_Name_Ch as spon from ( " \
    " select IRB_No, Manu_Name from signed_contract where Is_DC= 'N' " \
    " and Is_Intrust = 'Y' and Is_Required_Rpt = 'Y' and Execute_Id <> '0014') sc " \
    " left join " \
    " ( select Info_Id, Info_Name_Ch from basic_info where Info_Type = 'spon') as b " \
    " on sc.Manu_Name = b.Info_Id " \
    
        
    def connect_db(self):
        connection = None
        connection = mysql.connector.connect(**DataBase.connection_config_dict)
        return connection
    
    def query(self):
        result_df = None
        try:
            conn = self.connect_db()
            if conn.is_connected():
                result_df = pd.read_sql(DataBase.sql, conn)
                        
        except Error as e:
            print(f'資料庫操作發生問題 : {e}')
        except Exception as ex:
            print(f'資料查詢過程發生錯誤 : {ex}')
        finally:
            if conn is not None and conn.is_connected():
                conn.close()
                print('資料庫連線已關閉')
        
        return result_df
    
    # 查詢所有委託中心的案件
    def query_ctc_case(self):
        result_df = None
        DataBase.sql = " select IRB_No from signed_contract where Is_DC= 'N' " \
        " and Is_Intrust = 'Y' and Execute_Id <> '0014' " 
        
        try:
            conn = self.connect_db()
            if conn.is_connected():
                result_df = pd.read_sql(DataBase.sql, conn)
                        
        except Error as e:
            print(f'資料庫操作發生問題 : {e}')
        except Exception as ex:
            print(f'資料查詢過程發生錯誤 : {ex}')
        finally:
            if conn is not None and conn.is_connected():
                conn.close()
                print('資料庫連線已關閉')
        
        return result_df
    



def main():
    database = DataBase()
    spon_df = database.query()
    print("done")

if __name__ == '__main__':
    main()

