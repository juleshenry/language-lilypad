import pdfplumber
import re

class Defi:
    def __init__(_S, pala:str):
        setattr(_S, 'pala', pala)
        setattr(_S, 'defs', dict())
        # setattr(_S, pala, 'pala')

def extract_text_from_range(pdf_path, start_page, end_page):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        # 0-ix
        for page_num in range(start_page - 1, end_page):
            page = pdf.pages[page_num]
            text += page.extract_text()
    # '\d+\.'

    for o in text.split('->')[1:]: 
        matches = re.split(r'\(\d+\)',o)
        for k,kk in enumerate(matches):
            print('('*5,k+1,')'*5)
            _matches = re.split(r'\d+\.', kk)
            for i, j in enumerate(_matches):
                print(i,'~'*(i+3),j)
    return text

# Usage example
pdf_path ="src_langz/RAE_español.pdf"
start_page = 3
end_page = 5

extracted_text = extract_text_from_range(pdf_path, start_page, end_page)
s= Defi('aba')
# print(extracted_text)
print(vars(s))

# with open("src_langz/RAE_español.pdf", 'rb') as pdf_file:
#     # Create a PDF reader object
#     pdf_reader = PyPDF2.PdfReader(pdf_file)

#     # Initialize a PDF writer object
#     pdf_writer = PyPDF2.PdfFileWriter()

#     # Iterate through pages and add them to the writer
#     for page_num in range(43, 100):  # Page numbers are 0-based
#         page = pdf_reader.getPage(page_num)
#         pdf_writer.addPage(page)

#     # Create a new PDF file with the selected pages
#     with open('output.pdf', 'wb') as output_pdf:
#         pdf_writer.write(output_pdf)