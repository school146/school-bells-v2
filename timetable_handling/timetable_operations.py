from datetime import datetime
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from timetable_storage import TimetableStorage

def get_timetable(message):
    timetables = TimetableStorage('timetable')

    print(timetables.deserialize())

def add_unique_day(message):
    timetables = TimetableStorage('timetable')
    timetables.append_day(datetime.now())