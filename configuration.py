import sqlite3

connection = sqlite3.connect('database.db', check_same_thread=False)
owner = 'ncinsli'

time_table_name = 'bells'
overrided_time_table_name = 'bell_overrides'
admin_table_name = 'admins'
pre_ring_delta = 120

ring_duration = 3
pre_ring_duration = 1.5