# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:18:15 2022

@author: Bill
"""
from util.file_util import FileUtil
from util.str_util import StringUtil
from util.excel_util import ExcelUtil
from PyPDF2 import PdfFileWriter, PdfFileReader
from entity.db import DataBase
import log
import pdfplumber
import configparser

# 全域變數
#input_path = "pdf/11110-受試者編號.pdf"
#dir_path = r'pdf'

# 測試用
# input_path = "pdf/11102-受試者編號-測試2.pdf"
#network_drive_path = r"\\172.19.61.159\月報表明細"
#network_drive_path = r"\\172.19.61.159\月報表明細\test"
sub_history_dir = ""
#sub_history_dir = "歷年資料"
sub_spon_dir = ""
#sub_spon_dir = "廠商分類"
#excel_path = r"excel/2022年11月門診住院費.xlsx"
#excel_output_path = r"excel/2022年11月門診住院費更新.xlsx"

# 各IRB案件正確的門診金額
op_total_dict = {}

# 根據IRB編號取得廠商名稱
def get_sponsor_from_df(irb_no , df):
    result = None
    if irb_no in df.values:
        result = df.loc[df.IRB_No == irb_no , 'spon'].values[0]
        
        if StringUtil.has_substr(result, '阿斯特捷利康') or StringUtil.has_substr(result, 'AstraZeneca'):
            result = 'AZ'
        elif StringUtil.has_substr(result, '默沙東'):
            result = 'MSD'
        elif StringUtil.has_substr(result, '羅氏'):
            result = '羅氏'
        else:
            result = 'Other'        
    return result

# 取得各IRB 門診月報表明細總額
def get_op_month_total(payment_list):
    payment_total = ''
    # 月報表合計在最後一列  
    if payment_list is not None:
        # 合計在最後一列
        tmp_list = payment_list[-1]
        # 合計金額位於該列最後一欄
        if tmp_list[1] == "合計":
            payment_total = tmp_list[-1]
    return payment_total;

# pdf 檔案分割分類
def split_pdf(file_list, dest, df):
    page_list = []
    spon_list = []
    
    for src in file_list:
        #開啟pdf 檔案
        with open(src , 'rb') as f:        
            pdf = PdfFileReader(f)
            # 區域變數
            # PDF 總頁數
            pages = pdf.getNumPages()
            plumber_pdf = pdfplumber.open(f)
                    
            # 歷年資料的預設檔名
            prev_file_name = 'none.pdf'
            # 廠商分類的預設廠商名
            prev_spon = 'none'
            # IRB
            prev_irb = 'none'
            prev_id = 'none'
            
            
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
                manu_context = ''
                has_manu = False
                
                if(len(cur_page_context_ary) > 5):
                    manu_context = cur_page_context_ary[5]
                    # 檢查當前頁是否含有廠商代碼字樣
                    has_manu = StringUtil.has_substr(manu_context, '廠商代碼')
                            
                #有廠商代碼
                if has_manu:
                    # 子身分
                    regex = r'\d{2}'
                    sub_id = StringUtil.regex_match(manu_context, regex)
                    
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
                                    
                    # 分割後的新檔名: year_month_id_irb_pi.pdf
                    # 同案件可能有不同身分別故需要子身分作為檔名一部分避免檔案被覆寫
                    file_name = f'{year}_{month}_{sub_id}_{manu}_{irb}_{pi}.pdf'
                    
                    # 先輸出前面的頁面內容
                    if len(page_list) > 0:                                                                                                                                                        
                        
                        # 歷年資料依照IRB名稱分類的路徑: \\172.19.61.159\月報表明細\歷年資料\IRB編號
                        history_path = FileUtil.get_path(dest, sub_history_dir, f'{prev_irb}')
                        
                        # 建立資料夾存放歷年資料
                        FileUtil.create_dir(history_path)
                        history_path_str = FileUtil.get_path_str(history_path)
    
                        # 輸出文件
                        for i in page_list:                                                 
                            # 加入待輸出的頁數
                            pdf_writer.addPage(pdf.getPage(i))
                            
                            # 取出各頁表格資訊
                            # cur_page = page_list[i]
                            page_tb_content = plumber_pdf.pages[i].extract_table();
                            
                            # 取得每一IRB 案件的門診總金額並存入dict
                            op_total = get_op_month_total(page_tb_content)
                            
                            if(op_total != ''):
                                op_total = int(op_total.replace(',' , ''))
                                key = f'{prev_id}-{prev_irb}'
                                op_total_dict[key] = op_total
                                break                                                        
                                                
                        # 輸出文件路徑                                        
                        new_file_dest = FileUtil.get_path_str(
                            FileUtil.get_path(history_path_str, prev_file_name))
                        
                        # 產生分割後的新檔案
                        FileUtil.save_pdf(new_file_dest, pdf_writer)                                                                
                        
                        
                        # 若屬於委託中心且需月報表之案件多寫一份檔案到不同位置
                        if len(spon_list) > 0:
                            # 建立資料夾依照廠商名稱分類
                            sp = spon_list[0]
                            spon_path = FileUtil.get_path(dest, sub_spon_dir, f'{year}_{month}', f'{sp}')
                            FileUtil.create_dir(spon_path)
                            spon_path_str = FileUtil.get_path_str(spon_path)
                            
                            new_spon_file_dest = FileUtil.get_path_str(
                                FileUtil.get_path(spon_path_str, prev_file_name))
                            
                            # 產生分割後的新檔案
                            FileUtil.save_pdf(new_spon_file_dest, pdf_writer)
                            
                            # 清空廠商列表
                            spon_list.clear()
    
                                                                                         
                        # 清空 page 列表
                        page_list.clear()
                        page_list.append(page)
                        
                    else:
                        page_list.append(page)
                                                                                
                else:
                    # 內容跨頁
                    page_list.append(page)
                    
                prev_file_name = file_name
                prev_irb = irb
                prev_id = sub_id
                
                # 屬於委託中心且需月報表之案件儲存廠商名
                if sponsor is not None:
                    spon_list.append(sponsor)
            
            
                    
            # 檢查頁面清單是否還有未輸出的內容
            if len(page_list) > 0:
                
                pdf_writer = PdfFileWriter()
                
                for i in page_list:
                    pdf_writer.addPage(pdf.getPage(i))
                    
                    # 取出各頁表格資訊
                    page_tb_content = plumber_pdf.pages[i].extract_table();
                    
                    # 取得每一IRB 案件的門診總金額並存入dict
                    op_total = get_op_month_total(page_tb_content)
                    
                    if(op_total != ''):
                        op_total = int(op_total.replace(',' , ''))
                        key = f'{prev_id}-{prev_irb}'
                        op_total_dict[key] = op_total
                        break                                        
                
                # 歷年資料依照IRB名稱分類的路徑: \\172.19.61.159\月報表明細\歷年資料\IRB編號
                history_path = FileUtil.get_path(dest, sub_history_dir, f'{prev_irb}')
                # 建立資料夾存放歷年資料
                FileUtil.create_dir(history_path)
                history_path_str = FileUtil.get_path_str(history_path)
                
                new_file_dest = FileUtil.get_path_str(
                    FileUtil.get_path(history_path_str, prev_file_name))
                
                # 產生分割後的新檔案
                FileUtil.save_pdf(new_file_dest, pdf_writer)
                
                if len(spon_list) > 0:
                    # 建立資料夾依照廠商名稱分類
                    sp = spon_list[0]
                    spon_path = FileUtil.get_path(dest, sub_spon_dir, f'{year}_{month}', f'{sp}')
                    FileUtil.create_dir(spon_path)
                    spon_path_str = FileUtil.get_path_str(spon_path)
                    
                    new_spon_file_dest = FileUtil.get_path_str(
                        FileUtil.get_path(spon_path_str, prev_file_name))
                    
                    # 產生分割後的新檔案
                    FileUtil.save_pdf(new_spon_file_dest, pdf_writer)
                        
            # 清空 page 列表
            page_list.clear()
            
            # 清空物件
            pdf_writer  = None
            
        # 刪除檔案
        FileUtil.delete(src)
            
        # 用來檢查檔案已確實關閉
        # print(pdf.pages[0].extract_text())


if __name__ == '__main__':
    
    log.root_logger.info('開始取得設定檔參數')    
    config = configparser.ConfigParser()
    config.read('D:/op_report/conf/config.ini' , encoding='utf-8')
    
    network_drive_path = config['custom']['network_drive_path']
    pdf_dir_path = config['custom']['pdf_dir_path']
    
    sub_history_dir = config['custom']['pdf_history_dir']
    sub_spon_dir = config['custom']['pdf_spon_dir']
    excel_dir_path = config['custom']['excel_dir_path']
    new_report_path = config['custom']['new_report_path']
    
        
    log.root_logger.info('開始取得所有委託廠商資料集合')    
    database = DataBase()
    # 所有委託案件的廠商
    sponsors = database.query()
    
    log.root_logger.info('開始取得所有委託中心案件之IRB編號')
    ctc_case = database.query_ctc_case()    
    
    file_name_list = FileUtil.get_file_list(pdf_dir_path)
    
    # pdf 分類
    log.root_logger.info('開始 pdf 報表分類作業')
    split_pdf(file_name_list, network_drive_path, sponsors)        
    
    report_path = FileUtil.get_file_list(excel_dir_path)[0]
    df = ExcelUtil.get_df(report_path)
    
    log.root_logger.info('報表分類作業結束，開始更新錯誤的門診金額並產生新報表')
    print('報表分類作業結束，開始更新錯誤的門診金額')
    
    # 修正門診月報表金額
    try:
        ExcelUtil.update_data(op_total_dict, df, ctc_case)    

    except Exception as e:       
        log.root_logger.error(f'門診月報表金額修改過程發生錯誤: {e}')
        print('新報表產生失敗')
    else:
        log.root_logger.info('門診金額更新完成，準備產生新報表')    
        # 匯出成新檔案
        df.to_excel(new_report_path, sheet_name="門住診報表", index=False)    
        log.root_logger.info('新報表產生結束')
    finally:
        log.close_log()
    
    log.root_logger.info('測試訊息')
        
    

    
    
    
    
    