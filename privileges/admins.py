from privileges.status_codes import AppendAdminStatus, DeleteAdminStatus
import os
import sqlite3

table = 'admins'; connection = sqlite3.connect('database.db', check_same_thread=False); cursor : sqlite3.Cursor = connection.cursor()

def configure():
    exec_unsafe(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            userid TEXT UNIQUE
        ) 
        """)

# Выполнение SQL-запроса без возможности использовать защиту от инъекций (?)
def exec_unsafe(string: str) -> list:
    cursor.execute(string)
    content = cursor.fetchall()
    connection.commit()

    return content

def deserialize() -> object:
    content = exec_unsafe(f"SELECT * FROM {table}")[0]
    return content

def append_admin(id: str) -> AppendAdminStatus: # -> UserStorage
    id = str(id).replace('@', '').lower()

    try:
        cursor.execute(f"""
            INSERT INTO {table} VALUES(?)
        """, [id])    
        connection.commit()
        return AppendAdminStatus.OK

    except sqlite3.IntegrityError:
        return AppendAdminStatus.USER_ALREADY_EXISTS


def delete_admin(id: str) -> DeleteAdminStatus:
    id = str(id).replace('@', '').lower()    
    
    try:
        cursor.execute(f"""
            DELETE FROM {table} WHERE userid=?;
        """, [id])    
        connection.commit()    
        return DeleteAdminStatus.OK
    
    except:
        return DeleteAdminStatus.USER_NOT_ADMIN

def contains(id: str) -> bool:
    cursor.execute(f"SELECT * FROM {table} WHERE userid=?", [id])
    content = cursor.fetchone()
    connection.commit()

    return content is not None


