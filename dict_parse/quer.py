import sqlite3

conn = sqlite3.connect("palabras.db")


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
    # print('sarching4', palabra)
    cursor.execute(
        f"""
        SELECT definicion
        FROM palabras
        WHERE palabra = ?
    """,
        (palabra,),
    )
    defi = cursor.fetchone()
    # conn.close()
    if defi:
        return str(defi[0])
    else:
        return None





def loadall():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM palabras LIMIT 10")
    rows = cursor.fetchall()
    for a in rows:
        print(a[0], "\n", a[1], f'\n{"#"*100}')



def tokenize(defi:str):
    
    defi= defi.replace('\n',' ')
    limp = lambda x:x.replace('.','').replace(',','').replace('(','').replace(')','').replace('-','')
    return map(limp, defi.split(' '))

defi = query_palabra('monear')
print(defi)
# for o in tokenize(defi):
#     print('PALABRA',o)
#     print('DEFIIII',query_palabra(o))

# print(query_palabra('a'))
# with open('pax.txt') as p:
