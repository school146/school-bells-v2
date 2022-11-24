import os
import sqlite3

class UserStorage():
    table : str
    connection = None
    cursor = None

    def __init__(self, table: str):
        self.table = table
        
        self.connection = sqlite3.connect(f'database.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            userid TEXT UNIQUE
        ) 
        """)
        self.connection.commit()
        

    def deserialize(self) -> object:
        self.cursor.execute(f"SELECT * FROM {self.table}")
        content = self.cursor.fetchone()
        self.connection.commit()

        return content

    def append_user(self, id): # -> UserStorage
        id = str(id).replace('@', '').lower()

        try:
            self.cursor.execute(f"""
                INSERT INTO {self.table} VALUES(?)
            """, [id])    
            self.connection.commit()

        except sqlite3.IntegrityError:
            print("User already exits!")
        
        return self

    def remove_user(self, id):
        id = str(id).replace('@', '').lower()

        try:
            self.cursor.execute(f"""
                DELETE FROM {self.table} WHERE userid=?;
            """, [id])    
            self.connection.commit()

        except:
            print("User doesn't exist!")
        
        return self

    def contains(self, id: str):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE userid=?", [id])
        content = self.cursor.fetchone()
        self.connection.commit()
        print(content is not None)
        return content is not None

