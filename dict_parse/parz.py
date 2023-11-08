import pdfplumber
import re, sqlite3


class Pala:
    def __init__(_S, bra: str, defis: list):
        setattr(_S, "bra", bra)
        setattr(_S, "defis", defis)


class Dixionario:
    def __init__(_S):
        _S.palabras = list()

    def add(_S, x):
        _S.palabras.append(x)


def extract_text_from_range(pdf_path, start_page, end_page):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(start_page - 1, end_page):
            page = pdf.pages[page_num]
            text += page.extract_text()
    Dix = Dixionario()
    palabras = list(re.split(r"->(.*?)(?=\.)", text))[1:]
    for x, y in zip(palabras, palabras[1:]):  # skip intro trash
        bra, defis = x, y
        Dix.add(Pala(bra, defis))
        ########## Deeper, later, catch all cases well ####################
        # parens_ = re.split(r"\(\d+\)", palabra)
        # if len(parens_) > 1: # Weird case for the entry for 'a'
        #     p = Pala(parens_[0])
        #     for k, paren in enumerate(parens_[1:]):
        #         periodos_ = re.split(r"\d+\.", paren)
        #         origen = periodos_[0].replace('.','').strip()
        #         if not origen:
        #             origen = por_defecto
        #         p.defis[origen] = periodos_[1:]
        # else: # Typical case
        #     periodos_ = list(map(lambda x:x.strip(),re.split(r"\.", palabra)))
        #     p = Pala(periodos_[0])
        #     print(periodos_[0])
        #     print(periodos_[1:])
        #     p.defis[por_defecto] = periodos_[1:]
        ############################################################
    return Dix


# Usage example
pdf_path = "src_langz/RAE_español.pdf"
start_page = 3
end_page = 5 or 6348  # end of book
dix = extract_text_from_range(pdf_path, start_page, end_page)

conn = sqlite3.connect("palabras.db")
conn.execute(
    f"""
    CREATE TABLE IF NOT EXISTS palabras (
        palabra TEXT PRIMARY KEY,
        definicion TEXT
    )
"""
)

for pala in dix.palabras:
    conn.execute(
        f"""
        INSERT INTO palabras (palabra, definicion)
        VALUES (?, ?)
    """,
        (pala.bra, pala.defis),
    )


def query_palabra(palabra: str):
    """
    USED TO QUERY FOR THE WORD DEF
    
    Example usage
    ```
    definition = query_palabra("ababa")
    if definition:
        print(f"The definition for 'ababa' is: {definition}")
    else:
        print("No definition found for 'ababa'")
    ```
    """
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT definicion
        FROM palabras
        WHERE palabra = ?
    """,
        (palabra,),
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None
