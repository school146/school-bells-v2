from datetime import datetime
import calendar
import sqlite3 

# Will be injected by dynaconf
table = 'bells'
table_override = 'bell_overrides'

def get_time(connection: sqlite3.Connection, date: datetime):
    
    cursor = connection.cursor()

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
