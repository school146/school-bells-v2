import sqlite3

# Will be injected by dynaconf
table = 'admins'

def contains(id: str, connection: sqlite3.Connection) -> bool:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE userid=?", [id])
    content = cursor.fetchone()
    connection.commit()

    return content is not None