# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 14:09:26 2022

@author: Bill
"""
import re

class StringUtil:
    
    # 根據找出符合正則規則的文字內容
    @staticmethod
    def regex_match(context, pattern):
        result = 'unknown'
        regexPattern = re.compile(r'{}'.format(pattern))
        mo = regexPattern.search(context)
        if mo is not None:
            try:        
                result = mo.group()
            except Exception as ex:
                #print(f"正則比對過程發生錯誤:{ex}")
                result = 'unknown'
        return result
    
    # 檢查子字串是否包含在原始字串中
    @staticmethod
    def has_substr(origin , sub):
        return sub in origin
    
    
    
    