from timetable.events import EventType
from datetime import datetime
import timetable.utils
import timetable.getting
import configuration
import calendar
import sqlite3

# Will be injected by dynaconf
connection = configuration.connection
table = 'bells'
table_override = 'bell_overrides'

def resize(date: datetime, event: EventType, order: int, seconds: int): # -> UserStorage
    cursor = connection.cursor()

    default_timetable = timetable.getting.get_time(date)[0]
    new_timetable = default_timetable[:order - 1]

    for time in default_timetable[order - 1:]:
        result = timetable.utils.sum_times(time, seconds) if seconds >= 0 else timetable.utils.sub_times(time, abs(seconds))
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
