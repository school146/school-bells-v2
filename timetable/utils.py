from datetime import datetime

days = {0: u"Понедельник", 1: u"Вторник", 2: u"Среда", 3: u"Четверг", 4: u"Пятница", 5: u"Суббота", 6: u"Воскресенье"}

def get_weekday_russian(date_time: datetime):
    return days[date_time.weekday()].lower()

def time_literals_to_seconds(delta): # абревиатуры типа 2m превращает в 120секунд
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

def sum_times(initial_time: str, seconds: int):
    if seconds == 0: return initial_time
    hours = int(initial_time.split(':')[0])
    minutes = int(initial_time.split(':')[1])
    minutes += seconds // 60

    while minutes >= 60:
        minutes -= 60
        hours += 1

    return f'{hours}:{str(minutes).zfill(2)}'.zfill(5)

def sub_times(initial_time: str, seconds: int):
    if seconds == 0: return initial_time

    delta_mins = seconds // 60

    hours = int(initial_time.split(':')[0])
    minutes = int(initial_time.split(':')[1])
        
    minutes -= delta_mins

    while minutes < 0:
        minutes += 60
        hours -= 1

    return f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}'.zfill(5)