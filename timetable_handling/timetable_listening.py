from timetable_storage import TimetableStorage
from datetime import datetime

def listen():
    today = datetime.now().weekday()

    timetable_db = TimetableStorage('timetable')
    timetable_db