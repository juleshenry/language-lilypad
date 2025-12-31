"""
                                      :%&*+*=.       .==*%@+.                                       
                                     =@+=%*%*#-.....=%=*++&%#-                                      
                                     #%▒@█▓*==#&&&&&= █+▒░██#%                                      
                                     -▒&++&&.  .. .. .▓░++*#▒:                                      
                                     *%+*+:.   :- =:  ::&▒▒▓█&                                      
                                     @=*+****%+*&&&%*%%%%**%▓█                                      
                                     :%%=::::..++.-*==%*::=%%:                                      
                                      *██▒%:  --%▒@+%&██#▒██&                                       
                             .===++: =█#&░:.:.:=====#@▓███░░█* :=*+++.                              
                             &:.*==█░@- @▓..         . =▒█: :░@█+:. :▒-                             
                             @ =░▓▓▓▒::@█░            ..+#▒-.:▒███░*=█=                             
                             +░:.&██* :&█▒-             -@█@- ░██* =░&.                             
                              -░#@▓█▒.  :█▒:           :░█+ .&███%▒▓+                               
                     :==%&&░▒▒▒@▒▓▒██@- .-▓█&-       :&█▓+.=*██████▓░░░#***::.                      
               =+##@░@@&%*--     .&████#: #███▒&&%%&▒██▓*.:#████▒+::::%&&%#@▒░▒@%%=:                
            #@█░#*-.         ==%%@#@▓████+.*▒█████████▒% .▒████░▓█▓▒▒░▓=     .-==+#@▒@*:            
             .+*%@#▓▓░@@%%%%&░%░@#▒█&▒██@*%=#+▓%░█▓%░&=@:&%▓█▓@█&&%░@*▒@:           :+@█#:          
                   --*&#▒█░░░▒░%███%*█▓-*██-▒█#+▒██░+@█#*█▓-#▓@██▓▓░%▓&:         .     :░█=         
         :-+*%%%&%%%+=::.      . .:=++@&##&&@@+%*-+%&&&@##░#@+-=-. .:.                  :█&         
       *░█░%:                                                                         .+▒█+         
        .-*░▓▓@%+--                .                                              :-%@▓█#-          
            :-=%@▒▓▓##&%+--:                                            :---*%##░▓▓░#%=             
                  .-:%%%░▒▒▓█▓░@@@@#&&%&*%%%%%%%%%%*%**%%%%%%%%&#@@░░▒███▒▒▒&%&--.                  
                           ....++++&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&++++::::                          
            

                                 ▜                 ▜ ▘▜        ▌
                                 ▐ ▀▌▛▌▛▌▌▌▀▌▛▌█▌  ▐ ▌▐ ▌▌▛▌▀▌▛▌
                                 ▐▖█▌▌▌▙▌▙▌█▌▙▌▙▖  ▐▖▌▐▖▙▌▙▌█▌▙▌
                                       ▄▌    ▄▌         ▄▌▌     
"""

import pdfplumber
import re, sqlite3
import time

conn = sqlite3.connect("palabras.db")


class Pala:
    def __init__(_S, bra: str, defis: list):
        setattr(_S, "bra", bra)
        setattr(_S, "defis", defis)


class Dixionario:
    def __init__(_S):
        _S.palabras = dict()

    def add(_S, pala):
        _S.palabras[pala.bra] = pala.defis


def extract_text_from_range(pdf_path, start_page, end_page):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(start_page - 1, end_page):
            page = pdf.pages[page_num]
            text += page.extract_text()
    Dix = Dixionario()
    palabras = list(re.split(r"->(.*?)(?=\.)", text))[1:]
    for x, y in zip(palabras[::2], palabras[1::2]):  # skip intro trash
        bra, defis = x, y
        Dix.add(Pala(bra, defis))
    return Dix


# Usage example
def popula():
    pdf_path = "src_langz/RAE_español.pdf"
    start_page = 3
    end_page = 6348  # end of book
    # Create table, access
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS palabras (
            palabra TEXT PRIMARY KEY,
            definicion TEXT
        )
    """
    )
    dix = extract_text_from_range(pdf_path, start_page, end_page)

    # LOAD dictionary into SQL
    for lv in dix.palabras.items():
        try:
            palabra, defis = lv
            conn.execute(
                f"""
                INSERT INTO palabras (palabra, definicion)
                VALUES (?, ?)
            """,
                (palabra, defis),
            )
        except sqlite3.IntegrityError:  # word has two definitions
            pass
            # print(palabra, "has two definitions")
            # todo: append definicions

    # FETCH ALL SQLITE
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM palabras")
    rows = cursor.fetchall()
    for a in rows:
        print(a[0], "\n", a[1], f'\n{"#"*100}')
    # print(*, sep =)
    cursor.close()


s = time.time()
popula()
t = time.time()
print("total:", t - s)

#close commit
conn.commit()
conn.close()
