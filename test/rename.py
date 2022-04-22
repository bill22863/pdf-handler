import pdfplumber
import re


def regex_match(context, pattern):
    result = 'unknown'
    regexPattern = re.compile(r'{}'.format(pattern))
    mo = regexPattern.search(context)
    result = mo.group()
    return result

# 開啟pdf
def parse_file(path):
    with pdfplumber.open(path) as pdf:        
        first_page = pdf.pages[0]
        content_ary = first_page.extract_text().split("\n")
        
        regex = '\d{4}/\d{2}/\d{2}'
        date = regex_match(content_ary[4], regex)        
        year = date.split('/')[0]
        month = date.split('/')[1]
        
        # 廠商代碼、IRB、PI資訊在索引5
        manu_context = content_ary[5]
        # 廠商代碼
        regex = '[A-Za-z]{1}\d{3}'
        manu = regex_match(manu_context, regex)
        # IRB 編號
        regex = '[A-Z]+-[A-Z0-9]+-\d+-?\d*-?[A-Za-z]*'
        irb = regex_match(manu_context, regex)
        # PI
        regex = '[^A-Za-z0-9\-\：]{5,6}'
        pi = regex_match(manu_context, regex)
        
        file_name = f'{year}_{month}_{manu}_{irb}_{pi}.pdf'
        print(file_name)

if __name__ == '__main__':
    input_path = "pdf/11102-受試者編號.pdf"
    parse_file(input_path)
