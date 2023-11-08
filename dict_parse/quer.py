import sqlite3


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
        return result
    else:
        return None


def get_100():

    conn = sqlite3.connect("palabras.db")
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM palabras
    """
    )
    result = cursor.fetchone()
    if result:
        return result
    else:
        return None


x = get_100()
if x:
    for xx in x:
        print(xx)

# print(query_palabra('a'))
# with open('pax.txt') as p:
