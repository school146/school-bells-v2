from enum import Enum
import timetable_handling.utils as utils
from datetime import datetime
import calendar
import sqlite3
from timetable_handling.event_type import EventType
from timetable_handling.utils import sum_times, sub_times
import timetable_handling.timetable_defaultvalues

week = ["OnMonday", "OnTuesday", "OnWednesday", "OnThursday", "OnFriday", "OnSaturday", "OnSunday"]

connection = sqlite3.connect('database.db', check_same_thread=False)
table = 'bells'
table_override = 'bell_overrides'

cursor = connection.cursor()

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {table} (
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

connection.commit()
cursor.execute(f"""SELECT * FROM {table}""")
length = len(cursor.fetchall())

connection.commit()
if length == 0:
    timetable_defaultvalues.do_dirty_work(connection, cursor)

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {table_override} (
    id INTEGER,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    time TEXT NOT NULL,
    muted INTEGER DEFAULT 0,
    PRIMARY KEY(id AUTOINCREMENT)
) 
""")
connection.commit()


def set_bells(table):

    cursor.execute(f"DELETE FROM {table}")
    connection.commit()

    for key in table.keys():
        values = [key]
        try:
            sql = f'DELETE FROM {table} WHERE time ="{key}"'
            cursor.execute(sql)
        except: # сорян!
            pass

        for day in week:
            if table[key] != None:
                if day in table[key]:
                    values.append(1)
                else:
                    values.append(0)
            else:
                values = [key.zfill(5), 0, 0, 0, 0, 0, 0, 0]


        cursor.execute(f"""
            INSERT INTO {table}(time, OnMonday, OnTuesday, OnWednesday, OnThursday, OnFriday, OnSaturday, OnSunday) Values(?, ?, ?, ?, ?, ?, ?, ?)""", values)
        connection.commit()

def get_timetable(date: datetime):
    cursor.execute(f"""
        SELECT time, muted
        FROM {table_override}
        WHERE day={date.day} 
              AND month={date.month}
              AND year={date.year}
    """)

    content = cursor.fetchall()
    connection.commit()
    
    if content == []:
        # Значит на этот день распространяется обычное расписание
        columnName = 'On' + calendar.day_name[date.weekday()].capitalize()
        cursor.execute(f"""
            SELECT time, muted 
            FROM {table}
            WHERE {columnName}=1
        """)

        content = cursor.fetchall()
        connection.commit()
 
    prepared_content = []
    muted = []
    for time in content:
        prepared_content.append(time[0].zfill(2))
        muted.append(time[1])

    content = list(map(lambda e: str(e).zfill(2), prepared_content))
    return content, muted

def resize(date: datetime, event: EventType, order: int, seconds: int): # -> UserStorage

    default_timetable = get_timetable(date)[0]
    new_timetable = default_timetable[:order - 1]

    for time in default_timetable[order - 1:]:
        result = utils.sum_times(time, seconds) if seconds >= 0 else utils.sub_times(time, abs(seconds))
        new_timetable.append(result)

    try:
        dmy = f'{date.year}.{str(date.month).zfill(2)}.{str(date.day).zfill(2)}'
        columnName = 'On' + calendar.day_name[date.weekday()].capitalize()

        cursor.execute(f"""
                    SELECT muted FROM {table_override}
                    WHERE year={date.year}
                    AND month={date.month}
                    AND day={date.day}
                """)
        muted = list(map(lambda e: int(e[0]), cursor.fetchall()))
        connection.commit()

        if (len(muted) == 0):
            cursor.execute(f"""
                SELECT muted FROM {table}
                WHERE {columnName}=1
            """)
            muted = list(map(lambda e: e[0], cursor.fetchall()))
            connection.commit()


        for ring_time in default_timetable:
            cursor.execute(f"""
                    DELETE FROM {table_override}
                    WHERE year={date.year}
                    AND month={date.month}
                    AND day={date.day}
                    AND time="{ring_time}"
                """)
            connection.commit()

        print('New timetable', new_timetable)
        print('Muted', muted)
        for i in range(len(new_timetable)):
            cursor.execute(f"""
                    INSERT INTO {table_override}(year, month, day, time, muted) VALUES(?, ?, ?, ?, ?) 
                """, [date.year, date.month, date.day, new_timetable[i], muted[i]])
            connection.commit()

    except sqlite3.IntegrityError:
        print("Time already exits!")
    
    connection.commit()

def shift(date: datetime, mins: int):
    cursor.execute(f"""
        SELECT time
        FROM {table_override}
        WHERE year={date.year}
        AND month={date.month}
        AND day={date.day}
    """)
    content = cursor.fetchone()
    connection.commit()

    if content is None:
        # Значит на этот день ищем обычное расписание
        columnName = 'On' + calendar.day_name[date.weekday()].capitalize()

        cursor.execute(f"""
            SELECT time, muted 
            FROM {table}
            WHERE {columnName}=1
        """)
        content = cursor.fetchall()
        connection.commit()

        for copied in content:
            cursor.execute(f"""
                INSERT INTO {table_override}(year, month, day, time, muted) VALUES(?, ?, ?, ?, ?)
            """, [date.year, date.month, date.day, copied[0], copied[1]])

    resize(date, EventType.LESSON, 1, mins * 60)
    
def mute( date_time: datetime):
    time_str = str(date_time.time())[:5].zfill(5)
    timetable = get_timetable(date_time)[0]

    cursor.execute(f"""
    SELECT * FROM {table_override}
    WHERE time="{time_str}"
    """)
    overrides = cursor.fetchall()

    connection.commit()
    if len(overrides) == 0:
        # Значит этот день не был особенным, поэтому его надо таковым сделать
        for ring_time in timetable:
            cursor.execute(f"""
                    INSERT INTO {table_override}(year, month, day, time, muted) VALUES(?, ?, ?, ?, ?) 
                """, [date_time.year, date_time.month, date_time.day, ring_time, 1 if ring_time == time_str else 0])
            connection.commit()
    else:
        cursor.execute(f"""
            UPDATE {table_override}
            SET muted=1
            WHERE time="{time_str}"
        """)
        connection.commit()

    
def unmute(date_time: datetime):
    time_str = str(date_time.time())[:5].zfill(5)
    timetable = get_timetable(date_time)[0]

    cursor.execute(f"""
    SELECT * FROM {table_override}
    WHERE time="{time_str}"
    """)
    overrides = cursor.fetchall()
    connection.commit()

    if len(overrides) == 0:
        # Значит этот день не был особенным, поэтому его надо таковым сделать
        for ring_time in timetable:
            cursor.execute(f"""
                    INSERT INTO {table_override}(year, month, day, time, muted) VALUES(?, ?, ?, ?, ?) 
                """, [date_time.year, date_time.month, date_time.day, ring_time, 0 if ring_time == time_str else 1])
            connection.commit()
    else:
        cursor.execute(f"""
            UPDATE {table_override}
            SET muted=0
            WHERE time="{time_str}"
        """)
        connection.commit()

    return 
def contains( id: str):
    cursor.execute(f"SELECT * FROM {table} WHERE userid=?", [id])
    content = cursor.fetchone()
    connection.commit()
    return content is not None

def delete_overrides():
    cursor.execute(f"DELETE FROM {table_override}")
    connection.commit()
