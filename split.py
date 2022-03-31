# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:18:15 2022

@author: Bill
"""
from PyPDF2 import PdfFileWriter, PdfFileReader
import pdfplumber
import re

# 全域變數
# input_path = "pdf/11102-受試者編號.pdf"
input_path = "pdf/11102-受試者編號-測試2.pdf"
output_root_path = "split-pdf/"


def regex_match(context, pattern):
    result = 'unknown'
    regexPattern = re.compile(r'{}'.format(pattern))
    mo = regexPattern.search(context)
    try:        
        result = mo.group()
    except:
        result = 'unknown'
    return result

def contain_substr(origin , sub):
    return sub in origin

def split_pdf(src, dest):
    page_list = []
    
    #開啟pdf 檔案
    with open(src , 'rb') as f:        
        pdf = PdfFileReader(f)
        # 區域變數
        pages = pdf.getNumPages()
        plumber_pdf = pdfplumber.open(f)
        # need_merge = False
        
        # 輸出的檔名
        prev_file_name = 'unknown.pdf'
        # 下一頁
        next_page = 0
        
        for page in range(pages):
            # 建立PdfFileWriter 物件
            pdf_writer = PdfFileWriter()
                        
            # 當前頁面文本內容
            cur_page_context_ary = plumber_pdf.pages[page].extract_text().split('\n')
            
            # regex 規則
            regex = '\d{4}/\d{2}/\d{2}'
            # 日期資訊            
            date_context = regex_match(cur_page_context_ary[4], regex)
            # 年、月資訊
            year = date_context.split('/')[0]
            month = date_context.split('/')[1]
            
            # 廠商代碼、IRB、PI資訊在索引5
            manu_context = cur_page_context_ary[5]
            # 檢查當前頁是否含有廠商代碼字樣
            has_manu = contain_substr(manu_context, '廠商代碼')
            
            #有廠商代碼
            if has_manu:    
                # 廠商代碼
                regex = '[A-Za-z]{1}\d{3}'
                manu = regex_match(manu_context, regex)
                # IRB 編號
                regex = '[A-Z]+-[A-Z0-9]+-\d+-?\d*-?[A-Za-z]*'
                irb = regex_match(manu_context, regex)
                # PI
                regex = '[^A-Za-z0-9\-\：]{5,6}'
                pi = regex_match(manu_context, regex)
                
                # 分割後的新檔名: year_month_irb_pi.pdf
                file_name = f'{year}_{month}_{manu}_{irb}_{pi}.pdf'
                
                # 先輸出前面的頁面內容
                if len(page_list) > 0:
                    # 輸出文件
                    for i in page_list:
                        pdf_writer.addPage(pdf.getPage(i))                                        
                    
                    new_file_dest = f'{dest}{prev_file_name}'
                    # 產生分割後的新檔案
                    with open(new_file_dest , 'wb') as out :
                        pdf_writer.write(out)
                    
                    # 清空 page 列表
                    page_list.clear();
                    page_list.append(page)
                else:
                    page_list.append(page)
            else:
                # 內容跨頁
                page_list.append(page)
                
            prev_file_name = file_name
        
        # 檢查頁面清單是否還有未輸出的內容
        if len(page_list) > 0:
            
            for i in page_list:
                pdf_writer.addPage(pdf.getPage(i))                                        
            
            new_file_dest = f'{dest}{prev_file_name}'
            # 產生分割後的新檔案
            with open(new_file_dest , 'wb') as out :
                pdf_writer.write(out)
        
    # 用來檢查檔案已確實關閉
    # print(pdf.pages[0].extract_text())


if __name__ == '__main__':
    split_pdf(input_path, output_root_path)        