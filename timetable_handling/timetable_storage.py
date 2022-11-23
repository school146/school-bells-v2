import os
from enum import Enum
import sqlite3
from datetime import datetime
import calendar

class EventType(Enum):
    BREAK = 0
    LESSON = 1

class TimetableStorage():
    connection = None
    table = 'bells'
    table_override = 'bell_overrides'

    cursor = None

    def __init__(self):
        
        self.connection = sqlite3.connect(f'database.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            id INTEGER,
            time TEXT NOT NULL UNIQUE,
            OnMonday INTEGER DEFAULT 0,
            OnTuesday INTEGER DEFAULT 0,
            OnWednesday INTEGER DEFAULT 0,
            OnThursday INTEGER DEFAULT 0,
            OnFriday INTEGER DEFAULT 0,  
            OnSaturday INTEGER DEFAULT 0,
            OnSunday INTEGER DEFAULT 0,
            FromDay TEXT DEFAULT "01.09",
            TillDay TEXT  DEFAULT "31.05",
      	    PRIMARY KEY(id AUTOINCREMENT)
        ) 
        """)
        self.connection.commit()

        try:
            self.add_default_bells('8:30', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('8:50', 1) #2
            self.add_default_bells('9:00', 0, 1, 1, 1, 1, 0, 0) #3
           
            self.add_default_bells('9:15', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('9:35', 1) #2
            self.add_default_bells('9:45', 1, 1, 1, 1, 1, 0, 0) #3
           
            self.add_default_bells('9:25', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('9:55', 0, 1, 1, 1, 1, 0, 0) #3

            self.add_default_bells('10:10', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('10:30', 1) #2
            self.add_default_bells('10:40', 1, 1, 1, 1, 1, 0, 0) #3

            self.add_default_bells('10:20', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('10:50', 0, 1, 1, 1, 1, 0, 0) #3

            self.add_default_bells('11:05', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('11:35', 0, 1, 1, 1, 1, 0, 0) #3

            self.add_default_bells('11:25', 1, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('11:45', 1) #2
            self.add_default_bells('11:55', 0, 1, 1, 1, 1, 0, 0) #3

            self.add_default_bells('12:10', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('12:40', 0, 1, 1, 1, 1, 0, 0) #3

            self.add_default_bells('12:30', 1, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('12:50', 1) #2
            self.add_default_bells('13:00', 0, 1, 1, 1, 1, 0, 0) #3

            self.add_default_bells('13:15', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('13:35', 1) #2
            self.add_default_bells('13:45', 1, 1, 1, 1, 1, 0, 0) #3
            
            self.add_default_bells('13:25', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('13:55', 0, 1, 1, 1, 1, 0, 0) #3

            self.add_default_bells('14:10', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('14:30', 1) #2
            self.add_default_bells('14:40', 1, 1, 1, 1, 1, 0, 0) #3

            self.add_default_bells('14:15', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('14:50', 0, 1, 1, 1, 1, 0, 0) #3
                        
            self.add_default_bells('15:00', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('15:25', 1) #2
            self.add_default_bells('15:35', 0, 1, 1, 1, 1, 0, 0) #3

        except Exception as exception:
            print(exception)


        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table_override} (
            id INTEGER,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            time TEXT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT)
        ) 
        """)
        self.connection.commit()
        
    def add_default_bells(self, time, m, t = 0, w = 0, th = 0, f = 0, s = 0, su = 0):
        self.cursor.execute(f"""
                INSERT INTO {self.table}(time, OnMonday, OnTuesday, OnWednesday, OnThursday, OnFriday, OnSaturday, OnSunday) Values(?, ?, ?, ?, ?, ?, ?, ?)
            """, [time, m, t, w, th, f, s, su])
        self.connection.commit()


    def sum_times(self, initial_time: str, seconds: int):
        if seconds == 0: return initial_time

        hours = int(initial_time.split(':')[0])
        minutes = int(initial_time.split(':')[1])
        minutes += seconds // 60
        seconds %= 60

        hours += minutes // 60
        minutes %= 60

        return f'{hours}:{str(minutes).zfill(2)}'

    def sub_times(self, initial_time: str, seconds: int):
        if seconds == 0: return initial_time

        hours = int(initial_time.split(':')[0])
        minutes = int(initial_time.split(':')[1])
        minutes -= seconds // 60
        seconds = 60 - seconds

        hours -= minutes // 60
        minutes = 60 - minutes

        return f'{hours}:{str(minutes).zfill(2)}'

    def get_day(self, date: datetime):
        # weekday = calendar.day_name[day.weekday()]  #'Wednesday'
        self.cursor.execute(f"""
            SELECT (time)
            FROM {self.table_override}
            WHERE day={date.day} 
                  AND month={date.month}
                  AND year={date.year}
        """)

        content = self.cursor.fetchall()
        self.connection.commit()
        
        if content == []:
            columnName = 'On' + calendar.day_name[date.weekday()].capitalize()
            print(columnName)
            # Значит на этот день распространяется обычное расписание
            self.cursor.execute(f"""
                SELECT (time) 
                FROM {self.table}
                WHERE {columnName}=1
            """)

            content = self.cursor.fetchall()
            self.connection.commit()

        prepared_content = []
        
        for time in content:
            prepared_content.append(time[0])

        content = list(map(str, prepared_content))

        return content

    # Format hh:mm_lesson-duration_break-duration_long-break-duration
    def append_ring_shift(self, date: datetime, event: EventType, order: int, delta_sec: int): # -> UserStorage

        default_timetable = self.get_day(date)
        new_timetable = default_timetable[:order - 1]

        for time in default_timetable[order - 1:]:
            new_timetable.append(self.sum_times(time, delta_sec))

        print(default_timetable)
        print(new_timetable)

        try:
            dmy = f'{date.year}.{date.month}.{date.day}'
            
            for ring_time in new_timetable:
                self.cursor.execute(f"""
                        INSERT INTO {self.table_override}(year, month, day, time) VALUES(?, ?, ?, ?) 
                    """, [date.year, date.month, date.day, ring_time])
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
        return content is not None

