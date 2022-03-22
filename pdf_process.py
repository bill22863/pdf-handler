# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from win32com.client import DispatchEx

class Main:
    # constructor of Main class
    def __init__(self):
        # Initialization of the Strings
        self.excel_path = "D:/bill/python/PDF-Handler/src/11102-受試者編號.xls"
        self.pdf_path = "D:/bill/python/PDF-Handler/pdf/11102-受試者編號.pdf"

    # function of pdf generator
    def gen_pdf(self):
        #Open Excel application
        excel_app = DispatchEx("Excel.Application")
        #Run on background 
        excel_app.Visible = 0
        excel_app.DisplayAlerts = 0
        #Read Excel 
        wb = excel_app.Workbooks.Open(self.excel_path, False)
        work_sheet = wb.Worksheets[0]
        work_sheet.ExportAsFixedFormat(0, self.pdf_path)
        wb.Close()
        excel_app.Quit()
    
    def main(self):
        self.gen_pdf()

obj = Main()
obj.main()
        




