import sqlite3

# Will be injected by dynaconf
table = 'bells'
table_override = 'bell_overrides'

def set_time(connection: sqlite3.Connection, items):
    cursor = connection.cursor()

    cursor.execute(f"DELETE FROM {table}")
    connection.commit()

    for key in items.keys():
        values = [key]
        try:
            sql = f'DELETE FROM {table} WHERE time ="{key}"'
            cursor.execute(sql)
        except: # сорян!
            pass

        for day in ("OnMonday", "OnTuesday", "OnWednesday", "OnThursday", "OnFriday", "OnSaturday", "OnSunday"):
            if items[key] != None:
                if day in items[key]:
                    values.append(1)
                else:
                    values.append(0)
            else:
                values = [key.zfill(5), 0, 0, 0, 0, 0, 0, 0]


        cursor.execute(f"""
            INSERT INTO {table}(time, OnMonday, OnTuesday, OnWednesday, OnThursday, OnFriday, OnSaturday, OnSunday) Values(?, ?, ?, ?, ?, ?, ?, ?)""", values)
        connection.commit()

