import pyodbc

def connect_db():
    cursor = pyodbc.connect('DRIVER={PostgreSQL Unicode};'
                            'Server=XXX.XXX.XXX.XXX;'
                            'Port=XXXX;'
                            'DATABASE=#######;'
                            'UID=###########;'
                            'PWD=##########;')
    return cursor


def insert_found_product(cursor, data: dict, schemeTable: str):
    columns = tuple(data.keys())
    columns_str = ', '.join(columns)
    values = tuple(data.values())
    placeholders = ', '.join(['?' for _ in values])
    query = f"INSERT INTO {schemeTable} ({columns_str}) VALUES ({placeholders});"
    cursor.execute(query, values)
    cursor.commit()
    return 0

def check_code(cursor, code: str):
    cursor = cursor.cursor()
    query = f"SELECT * FROM public.chatcodes WHERE code = '{code}' AND usedTokens < maxTokens;"
    cursor.execute(query)
    try:
        rows = cursor.fetchall()[0]
        if int(rows[1]) > int(rows[2]):
            authorize = False
        else:
            authorize = True
    except:
        authorize = False
        rows = [0, 0, 0]
    #print(f"usedTokens: {rows[1]} - {rows[2]} -> {authorize}")
    return {"auth": authorize, "usedTokens": rows[1], "maxTokens": rows[2], "code": code}

def save_interaction(cursor, code: str, question: str, answer: str):
    data = {'code': code, 'pregunta': question, 'respuesta': answer}
    columns = tuple(data.keys())
    columns_str = ', '.join(columns)
    values = tuple(data.values())
    placeholders = ', '.join(['?' for _ in values])
    query = f"INSERT INTO public.chats ({columns_str}) VALUES ({placeholders});"
    cursor.execute(query, values)
    cursor.commit()
    return 0

def update_code(conn, code, tokens):
    cursor = conn.cursor()
    update_query = f"UPDATE public.chatcodes SET usedTokens = {tokens} WHERE code = '{code}';"
    cursor.execute(update_query)
    # Confirmar los cambios (commit)
    conn.commit()
