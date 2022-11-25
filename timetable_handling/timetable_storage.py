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
            time TEXT NOT NULL,
            OnMonday INTEGER DEFAULT 0,
            OnTuesday INTEGER DEFAULT 0,
            OnWednesday INTEGER DEFAULT 0,
            OnThursday INTEGER DEFAULT 0,
            OnFriday INTEGER DEFAULT 0,  
            OnSaturday INTEGER DEFAULT 0,
            OnSunday INTEGER DEFAULT 0,
            FromDay TEXT DEFAULT "01.09",
            TillDay TEXT  DEFAULT "31.05",
            muted INTEGER DEFAULT 0,
      	    PRIMARY KEY(id AUTOINCREMENT)
        ) 
        """)
        self.connection.commit()

        self.cursor.execute(f"""SELECT * FROM {self.table}""")
        length = len(self.cursor.fetchall())
        self.connection.commit()

        if length == 0:
            self.add_default_bells('08:30', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('08:50', 1) #2
            self.add_default_bells('09:00', 0, 1, 1, 1, 1, 0, 0) #3
           
            self.add_default_bells('09:15', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('09:35', 1) #2
            self.add_default_bells('09:45', 1, 1, 1, 1, 1, 0, 0) #3
           
            self.add_default_bells('09:25', 0, 0, 0, 0, 0, 1, 0) #1
            self.add_default_bells('09:55', 0, 1, 1, 1, 1, 0, 0) #3

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

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table_override} (
            id INTEGER,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            time TEXT NOT NULL,
            muted INTEGER DEFAULT 0,
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

        while minutes >= 60:
            minutes -= 60
            hours += 1

        return f'{hours}:{str(minutes).zfill(2)}'.zfill(5)

    def sub_times(self, initial_time: str, seconds: int):
        if seconds == 0: return initial_time

        delta_mins = seconds // 60

        hours = int(initial_time.split(':')[0])
        minutes = int(initial_time.split(':')[1])
        
        minutes -= delta_mins

        while minutes < 0:
            minutes += 60
            hours -= 1

        return f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}'.zfill(5)

    def get_timetable(self, date: datetime):
        self.cursor.execute(f"""
            SELECT time, muted
            FROM {self.table_override}
            WHERE day={date.day} 
                  AND month={date.month}
                  AND year={date.year}
        """)

        content = self.cursor.fetchall()
        self.connection.commit()
        
        if content == []:
            # Значит на этот день распространяется обычное расписание
            columnName = 'On' + calendar.day_name[date.weekday()].capitalize()
            self.cursor.execute(f"""
                SELECT time, muted 
                FROM {self.table}
                WHERE {columnName}=1
            """)

            content = self.cursor.fetchall()
            self.connection.commit()
    
        prepared_content = []
        muted = []
        for time in content:
            prepared_content.append(time[0].zfill(2))
            muted.append(time[1])

        content = list(map(lambda e: str(e).zfill(2), prepared_content))
        return content, muted

    def resize(self, date: datetime, event: EventType, order: int, seconds: int): # -> UserStorage

        default_timetable = self.get_timetable(date)[0]
        new_timetable = default_timetable[:order - 1]

        for time in default_timetable[order - 1:]:
            result = self.sum_times(time, seconds) if seconds >= 0 else self.sub_times(time, abs(seconds))
            new_timetable.append(result)

        try:
            dmy = f'{date.year}.{str(date.month).zfill(2)}.{str(date.day).zfill(2)}'
            
            self.cursor.execute(f"""
                        SELECT muted FROM {self.table_override}
                        WHERE year={date.year}
                        AND month={date.month}
                        AND day={date.day}
                    """)
            muted = list(map(lambda e: int(e[0]), self.cursor.fetchall()))
            print(muted)
            self.connection.commit()

            for ring_time in default_timetable:
                self.cursor.execute(f"""
                        DELETE FROM {self.table_override}
                        WHERE year={date.year}
                        AND month={date.month}
                        AND day={date.day}
                        AND time="{ring_time}"
                    """)
                self.connection.commit()

            for i in range(len(new_timetable)):
                self.cursor.execute(f"""
                        INSERT INTO {self.table_override}(year, month, day, time, muted) VALUES(?, ?, ?, ?, ?) 
                    """, [date.year, date.month, date.day, new_timetable[i], muted[i]])
                self.connection.commit()

        except sqlite3.IntegrityError:
            print("Time already exits!")
        
        self.connection.commit()
        return self

    def shift(self, date: datetime, mins):
        self.cursor.execute(f"""
            SELECT time
            FROM {self.table_override}
            WHERE year={date.year}
            AND month={date.month}
            AND day={date.day}
        """)
        content = self.cursor.fetchone()
        self.connection.commit()

        if content is None:
            # Значит на этот день ищем обычное расписание
            columnName = 'On' + calendar.day_name[date.weekday()].capitalize()

            self.cursor.execute(f"""
                SELECT time, muted 
                FROM {self.table}
                WHERE {columnName}=1
            """)
            content = self.cursor.fetchall()
            self.connection.commit()

            for copied in content:
                self.cursor.execute(f"""
                    INSERT INTO {self.table_override}(year, month, day, time, muted) VALUES(?, ?, ?, ?, ?)
                """, [date.year, date.month, date.day, copied[0], copied[1]])

        self.resize(date, EventType.LESSON, 1, mins * 60)
        
        return self

    def mute(self, date_time: datetime):
        time_str = str(date_time.time())[:5].zfill(5)
        timetable = self.get_timetable(date_time)[0]

        self.cursor.execute(f"""
        SELECT * FROM {self.table_override}
        WHERE time="{time_str}"
        """)
        overrides = self.cursor.fetchall()

        self.connection.commit()
        if len(overrides) == 0:
            # Значит этот день не был особенным, поэтому его надо таковым сделать
            for ring_time in timetable:
                self.cursor.execute(f"""
                        INSERT INTO {self.table_override}(year, month, day, time, muted) VALUES(?, ?, ?, ?, ?) 
                    """, [date_time.year, date_time.month, date_time.day, ring_time, 1 if ring_time == time_str else 0])
                self.connection.commit()
        else:
            self.cursor.execute(f"""
                UPDATE {self.table_override}
                SET muted=1
                WHERE time="{time_str}"
            """)
            self.connection.commit()

        return self

    def unmute(self, date_time: datetime):
        time_str = str(date_time.time())[:5].zfill(5)
        timetable = self.get_timetable(date_time)[0]

        self.cursor.execute(f"""
        SELECT * FROM {self.table_override}
        WHERE time="{time_str}"
        """)
        overrides = self.cursor.fetchall()
        self.connection.commit()

        if len(overrides) == 0:
            # Значит этот день не был особенным, поэтому его надо таковым сделать
            for ring_time in timetable:
                self.cursor.execute(f"""
                        INSERT INTO {self.table_override}(year, month, day, time, muted) VALUES(?, ?, ?, ?, ?) 
                    """, [date_time.year, date_time.month, date_time.day, ring_time, 0 if ring_time == time_str else 1])
                self.connection.commit()
        else:
            self.cursor.execute(f"""
                UPDATE {self.table_override}
                SET muted=0
                WHERE time="{time_str}"
            """)
            self.connection.commit()

        return self

    def contains(self, id: str):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE userid=?", [id])
        content = self.cursor.fetchone()
        self.connection.commit()
        return content is not None

