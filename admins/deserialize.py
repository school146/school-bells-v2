import sqlite3

# Will be injected by dynaconf
table = 'bells'
table_override = 'bell_overrides'

def deserialize(connection: sqlite3.Connection) -> object:
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    content = cursor.fetchall() # Strange
    connection.commit()
    return content