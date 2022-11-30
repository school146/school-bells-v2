import sqlite3

# Will be injected by dynaconf
table = 'bells'
table_override = 'bell_overrides'

def delete_all(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_override}")
    connection.commit()
