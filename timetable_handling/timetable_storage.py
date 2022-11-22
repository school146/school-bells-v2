import os
import sqlite3
from datetime import datetime
import calendar

class TimetableStorage():
    table : str
    connection = None
    cursor = None

    def __init__(self, table: str):
        self.table = table
        
        self.connection = sqlite3.connect(f'database.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            Monday TEXT,
            Tuesday TEXT,
            Wednesday TEXT,
            Thursday TEXT,
            Friday TEXT,
            Saturday TEXT
        ) 
        """)
        self.connection.commit()
        
        self.cursor.execute(f"SELECT * FROM {table} WHERE Monday!=NULL")
        result = self.cursor.fetchone()
        self.connection.commit()

        if result is None:
            self.cursor.execute(f"""
                INSERT INTO {self.table}(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) VALUES(?, ?, ?, ?, ?, ?)
            """, ['9:00'] * 6)

            self.connection.commit()

            for i in ('45', '10', '45', '10', '45', '20', '45', '20', '45', '10', '45', '10', '45', '10'):
                self.cursor.execute(f"INSERT INTO {self.table}(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) VALUES(?, ?, ?, ?, ?, ?)", [i] * 6)
                self.connection.commit()

    def deserialize(self) -> object:
        self.cursor.execute(f"SELECT * FROM {self.table}")
        content = self.cursor.fetchone()
        self.connection.commit()

        return content

    def get_day(self, day: datetime):
        
        weekday = calendar.day_name[day.weekday()]  #'Wednesday'

    # Format hh:mm_lesson-duration_break-duration_long-break-duration
    def append_day(self, day: datetime): # -> UserStorage

        try:
            column_name = f'"{day.day}.{day.month}.{day.year}"'

            self.cursor.execute(f"ALTER TABLE {self.table} ADD COLUMN {column_name} TEXT")    
            self.connection.commit()
            # return
        
            for i in ('9:00', '45', '10', '45', '10', '45', '20', '45', '20', '45', '10', '45', '10', '45', '10'):
                self.cursor.execute(f"INSERT INTO {self.table}({column_name}) VALUES(" + '"' + i + '"' + ")") #!
                self.connection.commit()

        except sqlite3.IntegrityError:
            print("User already exits!")
        
        self.connection.commit()
        return self

    # Format hh:mm_lesson-duration_break-duration_long-break-duration
    def remove_day(self, day: str): # -> UserStorage
        id = str(id).replace('@', '').lower()

        try:
            self.cursor.execute(f"""
                DELETE FROM {self.table} WHERE userid=?;
            """, [id])    
            self.connection.commit()

        except:
            print("User doesn't exist!")
        
        self.connection.commit()

        return self

    def contains(self, id: str):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE userid=?", [id])
        content = self.cursor.fetchone()
        self.connection.commit()
        print(content is not None)
        return content is not None

