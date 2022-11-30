import sqlite3

# Will be injected by dynaconf
table = 'bells'
table_override = 'bell_overrides'

def contains(connection: sqlite3.Connection, id: str) -> bool:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE userid=?", [id])
    content = cursor.fetchone()
    connection.commit()
    return content is not None

