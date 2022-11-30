from admins.status_codes import AppendAdminStatus, DeleteAdminStatus
import os
import sqlite3

table = 'admins'; connection = sqlite3.connect('database.db', check_same_thread=False); cursor : sqlite3.Cursor = connection.cursor()

def append(connection: sqlite3.Connection, id: str) -> AppendAdminStatus: # -> UserStorage
    id = str(id).replace('@', '').lower()
    cursor = connection.cursor()
    
    try:
        cursor.execute(f"""
            INSERT INTO {table} VALUES(?)
        """, [id])    
        connection.commit()
        return AppendAdminStatus.OK

    except sqlite3.IntegrityError:
        return AppendAdminStatus.USER_ALREADY_EXISTS

def delete(connection: sqlite3.Connection, id: str) -> DeleteAdminStatus:
    id = str(id).replace('@', '').lower()    
    cursor = connection.cursor()

    try:
        cursor.execute(f"""
            DELETE FROM {table} WHERE userid=?;
        """, [id])    
        connection.commit()    
        return DeleteAdminStatus.OK
    
    except:
        return DeleteAdminStatus.USER_NOT_ADMIN

