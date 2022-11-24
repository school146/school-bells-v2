from timetable_handling.timetable_storage import EventType
from datetime import datetime
from telebot import TeleBot
import calendar
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from timetable_storage import TimetableStorage

def get_timetable(bot: TeleBot, message):
    timetables = TimetableStorage()
    decomposed = message.text.split()
    if len(decomposed) == 1: 
        dmy = str(datetime.now().date()).split('-')
    else:
        dmy = (decomposed[1].split('.'))
        dmy.reverse()

    print(dmy)
    date = datetime(int(dmy[0]), int(dmy[1]), int(dmy[2]))
    
    list_db = timetables.get_day(date)
    combined = []

    for i in range(0, len(list_db) - 1):
        combined.append(list_db[i] + ' — ' + list_db[i + 1])


    to_out = (' ' * 4 + '\n').join(combined)

    bot.reply_to(message, f"""
    Расписание на {dmy[2]}.{dmy[1]}.{dmy[0]}:\n{to_out}
    """)
    


# /add_unique dd.mm.yyyy lesson 1 +20min
def add_rule_shift(message):
    
    decomposed = message.text.split()
    print(decomposed)
    day = int(decomposed[1].split('.')[0])
    month = int(decomposed[1].split('.')[1])
    year = int(decomposed[1].split('.')[2])

    type = decomposed[2]
    order = int(decomposed[3])
    delta = decomposed[4]
    delta_seconds = 0
    occurence = delta.find(next(filter(str.isalpha, delta)))

    measured_value = int(delta[:occurence])
    measure = delta[occurence:]
    
    if measure == 's': delta_seconds = measured_value
    if measure == 'min': delta_seconds = measured_value * 60
    if measure == 'h': delta_seconds = measured_value * 3600

    dmy = decomposed[1].split('.')
    date = datetime(int(dmy[2]), int(dmy[1]), int(dmy[0]))

    if type == 'lesson':
        timetables = TimetableStorage()
        timetables.append_ring_shift(date, EventType.LESSON, order * 2, delta_seconds)
    
    if type == 'break':
        timetables = TimetableStorage()
        timetables.append_ring_shift(date, EventType.BREAK, order * 2 + 1, delta_seconds)

def shift(bot: TeleBot, message):
    decomposed = message.text.split()
    print(decomposed)
    day = int(decomposed[1].split('.')[0])
    month = int(decomposed[1].split('.')[1])
    year = int(decomposed[1].split('.')[2])

    delta = decomposed[2]
    delta_seconds = 0
    occurence = delta.find(next(filter(str.isalpha, delta)))

    measured_value = int(delta[:occurence])
    measure = delta[occurence:]
    
    if measure == 's': delta_seconds = measured_value
    if measure == 'min': delta_seconds = measured_value * 60
    if measure == 'h': delta_seconds = measured_value * 3600


    print(delta_seconds)
    TimetableStorage().shift(datetime(year, month, day), delta_seconds // 60)
    bot.reply_to(message, f'Расписание на {day}.{month}.{year} сдвинуто на {delta_seconds // 60} мин')