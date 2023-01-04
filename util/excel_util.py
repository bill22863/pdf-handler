# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 10:26:03 2022

@author: Bill
"""

import pandas as pd

class ExcelUtil:
    
    # Excel 轉成 DataFrame
    @staticmethod
    def get_df(src):
        df = pd.read_excel(src,
                           converters={'子身分': str},
                           sheet_name="門住診報表")
        return df
        
    
    # 根據受試者月報表明細修改Excel 門診金額
    @staticmethod
    def update_data(payment_dict, op_df, ctc_df):
        # 資料筆數
        row_cnt = op_df[op_df.columns[0]].count()
        
        # 新增標題
        op_df['狀態'] = ['無'] * row_cnt
        op_df['案件類型'] = ['非委託'] * row_cnt
        
        # 檢查集合用以判斷重複案件
        chk_set = set()
        
        for i, row in op_df.iterrows():
            # 取得檔案中各案件的門診費用
            tmp_op_payment = row['門診']
            sub_id = row['子身分']
            irb = row['IRB編號']
            k = f'{sub_id}-{irb}'
            
            # 判斷案件類型
            if irb in ctc_df.values:
                op_df.at[i, '案件類型'] = '委託'

                if k not in chk_set:                           
                    if(k in payment_dict):
                        # 金額不相等則更新
                        if(payment_dict.get(k) != tmp_op_payment):
                            op_df.at[i, '門診'] = payment_dict.get(k)
                            # 更新註記
                            op_df.at[i, '狀態'] = '金額已修改'
                    else:
                        # 若屬於委託中心案件，則修改狀態
                        op_df.at[i, '狀態'] = '案件已刪除'
                        
                else:
                    op_df.at[i, '狀態'] = '案件已重複'
                
            # 檢查過後加入集合
            chk_set.add(k)
                    
            
            
        
        
        