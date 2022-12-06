import os
import sqlite3
import configuration
from admins.status_codes import AppendAdminStatus, DeleteAdminStatus

connection = configuration.connection
table = configuration.admin_table_name

def append(id: str) -> AppendAdminStatus: # -> UserStorage
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

def delete(id: str) -> DeleteAdminStatus:
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

