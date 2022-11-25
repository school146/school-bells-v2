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

def time_literals_to_seconds(in_seconds): # абревиатуры типа 2m превращает в 120секунд
    in_seconds = 0
    occurence = delta.find(next(filter(str.isalpha, delta)))

    measured_value = int(delta[:occurence])
    measure = delta[occurence:]

    if measure == 's': in_seconds = measured_value
    if measure == 'min': in_seconds = measured_value * 60
    if measure == 'h': in_seconds = measured_value * 3600

    return in_seconds

def is_time_format(timeArg):
    # TODO: написать
    return timeArg
