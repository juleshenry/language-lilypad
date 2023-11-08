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
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM palabras
        LIMIT 100
    """
    )
    result = cursor.fetchone()
    if result:
        return result
    else:
        return None


def loadall():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM palabras")
    rows = cursor.fetchall()
    for a in rows:
        print(a[0], "\n", a[1], f'\n{"#"*100}')

loadall()

# print(query_palabra('a'))
# with open('pax.txt') as p:
