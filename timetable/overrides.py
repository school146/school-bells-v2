import sqlite3
import configuration

table_override = configuration.overrided_time_table_name
table = configuration.time_table_name
connection = configuration.connection

def delete_all():
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_override}")
    connection.commit()
