import sqlite3
import calendar
import configuration
import timetable.resizing
from datetime import datetime
from timetable.events import EventType


table_override = configuration.overrided_time_table_name
table = configuration.time_table_name
connection = configuration.connection

def shift(date: datetime, mins: int):
    cursor = connection.cursor()
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

    timetable.resizing.resize(date, EventType.LESSON, 1, mins * 60)
    