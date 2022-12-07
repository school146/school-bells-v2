import sqlite3
import calendar
import timetable.getting
import timetable.muting
import timetable.shifting
from datetime import datetime
import timetable.middleware
import configuration

table_override = configuration.overrided_time_table_name
table = configuration.time_table_name
connection = configuration.connection

def mute(date_time: datetime):
    cursor = connection.cursor()

    time_str = str(date_time.time())[:5].zfill(5)
    timetable_today = timetable.getting.get_time(date_time)[0]

    cursor.execute(f"""
    SELECT * FROM {table_override}
    WHERE time="{time_str}"
    """)
    overrides = cursor.fetchall()

    connection.commit()
    if len(overrides) == 0:
        # Значит этот день не был особенным, поэтому его надо таковым сделать
        for ring_time in timetable_today:
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
    cursor = connection.cursor()

    time_str = str(date_time.time())[:5].zfill(5)
    timetable_today = timetable.getting.get_time(date_time)[0]

    cursor.execute(f"""
    SELECT * FROM {table_override}
    WHERE time="{time_str}"
    """)
    overrides = cursor.fetchall()
    connection.commit()

    if len(overrides) == 0:
        # Значит этот день не был особенным, поэтому его надо таковым сделать
        for ring_time in timetable_today:
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
