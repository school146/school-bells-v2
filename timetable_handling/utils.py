from datetime import datetime

days = {0: u"Понедельник", 1: u"Вторник", 2: u"Среда", 3: u"Четверг", 4: u"Пятница", 5: u"Суббота", 6: u"Воскресенье"}

def get_weekday_russian(date_time: datetime):
    return days[date_time.weekday()].lower()