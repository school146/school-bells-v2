from datetime import datetime
from timetable_storage import TimetableStorage
from daemon.daemon import Daemon

days = {0: u"Понедельник", 1: u"Вторник", 2: u"Среда", 3: u"Четверг", 4: u"Пятница", 5: u"Суббота", 6: u"Воскресенье"}

def get_weekday_russian(date_time: datetime):
    return days[date_time.weekday()].lower()

# Отправляет демону нужные колбэки
def apply(daemon: Daemon, date: datetime):
    updated_table, updated_mutedtable = TimetableStorage().get_timetable(date)
    daemon.update(updated_table, updated_mutedtable)