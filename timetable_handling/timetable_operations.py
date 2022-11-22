from datetime import datetime
import calendar
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from timetable_storage import TimetableStorage

def get_timetable(message):
    timetables = TimetableStorage('timetable')

    print(timetables.deserialize())

def add_unique_day(message):
    day = message.text.split()[1]

    if day.count('.') != 2: return

    dmy = day.split('.')
    date = datetime(int(dmy[2]), int(dmy[1]), int(dmy[0]))
    timetables = TimetableStorage('timetable')
    timetables.append_day(date)