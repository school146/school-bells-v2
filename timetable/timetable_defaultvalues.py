import configuration
# Will be deprecated soon

table_override = configuration.overrided_time_table_name
table = configuration.time_table_name
connection = configuration.connection

def add_default_bells(con, cursor, time, m, t = 0, w = 0, th = 0, f = 0, s = 0, su = 0):
    cursor.execute(f"""
            INSERT INTO {'bells'}(time, OnMonday, OnTuesday, OnWednesday, OnThursday, OnFriday, OnSaturday, OnSunday) Values(?, ?, ?, ?, ?, ?, ?, ?)
        """, [time, m, t, w, th, f, s, su])
    connection.commit()

def do_dirty_work():
    con = connection
    cur = connection.cursor()

    add_default_bells(con, cur, '08:30', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '08:50', 1) #2
    add_default_bells(con, cur, '09:00', 0, 1, 1, 1, 1, 0, 0) #3
   
    add_default_bells(con, cur, '09:15', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '09:35', 1) #2
    add_default_bells(con, cur, '09:45', 1, 1, 1, 1, 1, 0, 0) #3
   
    add_default_bells(con, cur, '09:25', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '09:55', 0, 1, 1, 1, 1, 0, 0) #3
    add_default_bells(con, cur, '10:10', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '10:30', 1) #2
    add_default_bells(con, cur, '10:40', 1, 1, 1, 1, 1, 0, 0) #3
    add_default_bells(con, cur, '10:20', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '10:50', 0, 1, 1, 1, 1, 0, 0) #3
    add_default_bells(con, cur, '11:05', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '11:35', 0, 1, 1, 1, 1, 0, 0) #3
    add_default_bells(con, cur, '11:25', 1, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '11:45', 1) #2
    add_default_bells(con, cur, '11:55', 0, 1, 1, 1, 1, 0, 0) #3
    add_default_bells(con, cur, '12:10', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '12:40', 0, 1, 1, 1, 1, 0, 0) #3
    add_default_bells(con, cur, '12:30', 1, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '12:50', 1) #2
    add_default_bells(con, cur, '13:00', 0, 1, 1, 1, 1, 0, 0) #3
    add_default_bells(con, cur, '13:15', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '13:35', 1) #2
    add_default_bells(con, cur, '13:45', 1, 1, 1, 1, 1, 0, 0) #3
    
    add_default_bells(con, cur, '13:25', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '13:55', 0, 1, 1, 1, 1, 0, 0) #3
    add_default_bells(con, cur, '14:10', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '14:30', 1) #2
    add_default_bells(con, cur, '14:40', 1, 1, 1, 1, 1, 0, 0) #3
    add_default_bells(con, cur, '14:15', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '14:50', 0, 1, 1, 1, 1, 0, 0) #3
                
    add_default_bells(con, cur, '15:00', 0, 0, 0, 0, 0, 1, 0) #1
    add_default_bells(con, cur, '15:25', 1) #2
    add_default_bells(con, cur, '15:35', 0, 1, 1, 1, 1, 0, 0) #3