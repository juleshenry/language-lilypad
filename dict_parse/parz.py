import pdfplumber
import re

class Pala:
    def __init__(_S, bra:str):
        setattr(_S, 'bra', bra)
        setattr(_S, 'origenes', list())
        setattr(_S, 'definiciones', dict())
        # setattr(_S, pala, 'pala')
    def __repr__(_S):
        print(_S.bra)
        for k,v in _S.definiciones.items():
            print('ORIGEN',k)
            print(*enumerate(v),sep='\n')
        return ""
def extract_text_from_range(pdf_path, start_page, end_page):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        # 0-ix
        for page_num in range(start_page - 1, end_page):
            page = pdf.pages[page_num]
            text += page.extract_text()
    # '\d+\.'

    for o in text.split('->')[1:]:
        pala = Pala
        matches = re.split(r'\(\d+\)',o)
        for k,kk in enumerate(matches):
            if not k:
                print('definición: ')
            else:
                print()#'('*5,k+1,')'*5)
            _matches = re.split(r'\d+\.', kk)
            for i, j in enumerate(_matches):
                if not i:
                    if not k:
                        pala = pala(j)
                        print(pala.bra)
                    else:
                        print('origen:', j)
                        pala.origenes.append(j)
                else:
                    print(i,'~'*(i+3),j)
                    o = pala.origenes[-1]
                    if pala.definiciones.get(o):
                        pala.definiciones[o].append(j)
                    else:
                        pala.definiciones[o] = [j]
        print(pala) #vars(pala));break
        break
    return text

# Usage example
pdf_path ="src_langz/RAE_español.pdf"
start_page = 3
end_page = 5 or 6348 # end of book

extracted_text = extract_text_from_range(pdf_path, start_page, end_page)
s= Pala('aba')
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