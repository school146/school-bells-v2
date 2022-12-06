import sqlite3

connection = sqlite3.connect('database.db', check_same_thread=False)
owner = 'ncinsli'

time_table_name = 'bells'
overrided_time_table_name = 'bell_overrides'
admin_table_name = 'admins'