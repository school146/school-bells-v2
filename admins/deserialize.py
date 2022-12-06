import sqlite3
import configuration

table = configuration.time_table_name
table_override = configuration.overrided_time_table_name
connection = configuration.connection

def deserialize() -> object:
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    content = cursor.fetchall() # Strange
    connection.commit()
    return content

