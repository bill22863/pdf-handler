# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:18:15 2022

@author: Bill
"""
from util.file_util import FileUtil
from util.str_util import StringUtil
from PyPDF2 import PdfFileWriter, PdfFileReader
import pdfplumber


# 全域變數
# input_path = "pdf/11102-受試者編號.pdf"
input_path = "pdf/11102-受試者編號-測試.pdf"
output_root_path = "split-pdf/"
network_drive_path = r"\\172.19.61.159\月報表明細"
sub_history_dir = "歷年資料"
sub_spon_dir = "廠商分類"


def get_sponsor_from_df(irb_no , df):
    result = None
    if irb_no in df.values:
        result = df.loc[df.IRB_No == irb_no , 'spon'].values[0]
        
    if StringUtil.has_substr(result, '阿斯特捷利康') or StringUtil.has_substr(result, 'AstraZeneca'):
        result = 'AZ'
    elif StringUtil.has_substr(result, '默沙東'):
        result = 'MSD'
    else:
        result = 'Other'        
    return result


def split_pdf(src, dest, df):
    page_list = []
    
    #開啟pdf 檔案
    with open(src , 'rb') as f:        
        pdf = PdfFileReader(f)
        # 區域變數
        pages = pdf.getNumPages()
        plumber_pdf = pdfplumber.open(f)
        
        # 輸出的檔名
        prev_file_name = 'unknown.pdf'
        
        for page in range(pages):
            # 建立PdfFileWriter 物件
            pdf_writer = PdfFileWriter()
                        
            # 當前頁面文本內容
            cur_page_context_ary = plumber_pdf.pages[page].extract_text().split('\n')
            
            # regex 規則
            regex = '\d{4}/\d{2}/\d{2}'
            # 日期資訊            
            date_context = StringUtil.regex_match(cur_page_context_ary[4], regex)
            # 年、月資訊
            year = date_context.split('/')[0]
            month = date_context.split('/')[1]
            
            # 廠商代碼、IRB、PI資訊在索引5
            manu_context = cur_page_context_ary[5]
            # 檢查當前頁是否含有廠商代碼字樣
            has_manu = StringUtil.has_substr(manu_context, '廠商代碼')
            
            # 建立資料夾存放歷年資料
            # 路徑: \\172.19.61.159\月報表明細\歷年資料\2022_02\
            FileUtil.create_dir(dest, sub_history_dir, f'{year}_{month}')
            
            #有廠商代碼
            if has_manu:    
                # 廠商代碼
                regex = '[A-Za-z]{1}\d{3}'
                manu = StringUtil.regex_match(manu_context, regex)
                # IRB 編號
                regex = '[A-Z]+-[A-Z0-9]+-\d+-?\d*-?[A-Za-z]*'
                irb = StringUtil.regex_match(manu_context, regex)
                # PI
                regex = '[^A-Za-z0-9\-\：]{5,6}'
                pi = StringUtil.regex_match(manu_context, regex)
                
                # 根據IRB編號取得廠商名稱
                sponsor = get_sponsor_from_df(irb, df)
                # 建立資料夾依照廠商名稱分類
                FileUtil.create_dir(dest, sub_spon_dir, f'{year}_{month}', f'{sponsor}')
                
                # 分割後的新檔名: year_month_irb_pi.pdf
                file_name = f'{year}_{month}_{manu}_{irb}_{pi}.pdf'
                
                # 先輸出前面的頁面內容
                if len(page_list) > 0:
                    # 輸出文件
                    for i in page_list:
                        pdf_writer.addPage(pdf.getPage(i))                                        
                    
                    new_file_dest = f'{dest}{prev_file_name}'
                    # 產生分割後的新檔案
                    FileUtil.save_pdf(new_file_dest, pdf_writer)
                        
                    #測試另外多寫一份檔案到不同位置
# =============================================================================
#                     output_copy_path = "split-merge/"
#                     new_file_dest_copy = f'{output_copy_path}{prev_file_name}'
#                     with open(new_file_dest_copy, 'wb') as copy_out:
#                         pdf_writer.write(copy_out)
# =============================================================================
                    
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
            FileUtil.save_pdf(new_file_dest, pdf_writer)

        
    # 用來檢查檔案已確實關閉
    # print(pdf.pages[0].extract_text())


if __name__ == '__main__':
    # 建立資料夾存放歷年資料
    # create_dir(network_drive_path , sub_history_dir , f'{m}月', '默沙東')
    split_pdf(input_path, network_drive_path)        