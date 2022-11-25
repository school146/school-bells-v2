from timetable_handling.timetable_storage import EventType
from datetime import datetime
from telebot import TeleBot
import json
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from timetable_storage import TimetableStorage
from daemon.daemon import Daemon
import utils

def get_timetable_middleware(bot: TeleBot, message, daemon: Daemon):
    timetables = TimetableStorage()
    decomposed = message.text.split()
    if len(decomposed) == 1: 
        dmy = str(datetime.now().date()).split('-')
    else:
        dmy = (decomposed[1].split('.'))
        dmy.reverse()

    date = datetime(int(dmy[0]), int(dmy[1]), int(dmy[2]))
    
    list_db, muted = timetables.get_timetable(date)
    combined = []

    for i in range(0, len(list_db) - 1):
        if i % 2 == 0:
            to_append = '<b>• ' + list_db[i] + ' — ' + list_db[i + 1] + '</b>'
        else: to_append = '   ' + list_db[i] + ' — ' + list_db[i + 1]

        if muted[i] == 1: 
            to_append = '🔇' + to_append
            if i > 0: 
                combined[i - 1] += '🔇'
        
        combined.append(to_append)

    bot.parse_mode = 'HTML'
    to_out = (' ' * 4 + '\n').join(combined)

    bot.reply_to(message, f"""
    🗓 Расписание на <b>{utils.get_weekday_russian(date)}, {date.day}</b>:\n\n{to_out}
    """)

def set_timetable_middleware(bot: TeleBot, message, daemon: Daemon):
    file_name = message.document.file_name
    file_id = message.document.file_name
    file_id_info = bot.get_file(message.document.file_id)

    content = bot.download_file(file_id_info.file_path).decode('utf-8')
    print(content) # Текст файла
    # TODO: Загрузка json -> изменение дефолтной БД (+ скопировать старую, наверное)

    utils.apply(daemon, datetime(datetime.now().year, datetime.now().month, datetime.now().day))

def resize_middleware(message, daemon: Daemon):
    args = message.text.split()[1:]
    day = int(args[0].split('.')[0])
    month = int(args[0].split('.')[1])
    year = int(args[0].split('.')[2])

    type = args[1]
    order = int(args[2])
    delta = args[3]
    
    in_seconds = 0
    occurence = delta.find(next(filter(str.isalpha, delta)))

    measured_value = int(delta[:occurence])
    measure = delta[occurence:]
    
    if measure == 's': in_seconds = measured_value
    if measure == 'min': in_seconds = measured_value * 60
    if measure == 'h': in_seconds = measured_value * 3600

    dmy = args[0].split('.')
    date = datetime(int(dmy[2]), int(dmy[1]), int(dmy[0]))

    if type == 'lesson':
        timetables = TimetableStorage()
        timetables.resize(date, EventType.LESSON, order * 2, in_seconds)

    if type == 'break':
        timetables = TimetableStorage()
        timetables.resize(date, EventType.BREAK, order * 2 + 1, in_seconds)

    utils.apply(daemon, datetime(year, month, day))

def shift_middleware(bot: TeleBot, message, daemon: Daemon):
    args = message.text.split()[1:]

    day = int(args[0].split('.')[0])
    month = int(args[0].split('.')[1])
    year = int(args[0].split('.')[2])

    delta = args[1]
    in_seconds = 0
    postfix_index = delta.find(next(filter(str.isalpha, delta)))

    measured_value = int(delta[:postfix_index])
    postfix = delta[postfix_index:]
    
    if postfix == 's': in_seconds = measured_value
    if postfix == 'min': in_seconds = measured_value * 60
    if postfix == 'h': in_seconds = measured_value * 3600

    TimetableStorage().shift(datetime(year, month, day), in_seconds // 60)
    bot.reply_to(message, f'Расписание на {utils.get_weekday_russian(datetime(year, month, day))}, {day} {month}, {year} сдвинуто на {in_seconds // 60} мин')

    utils.apply(daemon, datetime(year, month, day))

# /mute dd.mm.yyyy hh:mm
def mute_middleware(bot: TeleBot, message, daemon: Daemon):
    args = message.text.split()[1:]

    day = int(args[0].split('.')[0])
    month = int(args[0].split('.')[1])
    year = int(args[0].split('.')[2])

    number = args[1]
    hour = int(number.split(':')[0])
    minutes = int(number.split(':')[1])

    # Сериализация
    TimetableStorage().mute(datetime(year, month, day, hour, minutes))
    bot.reply_to(message, f'Звонок в {hour}:{minutes} {day}.{month}.{year} не будет включён')

    utils.apply(daemon, datetime(year, month, day))

def unmute_middleware(bot: TeleBot, message, daemon: Daemon):
    args = message.text.split()[1:]

    day = int(args[0].split('.')[0])
    month = int(args[0].split('.')[1])
    year = int(args[0].split('.')[2])

    number = args[1]
    hour = int(number.split(':')[0])
    minutes = int(number.split(':')[1])

    # Сериализация
    TimetableStorage().unmute(datetime(year, month, day, hour, minutes))
    bot.reply_to(message, f'Звонок в {hour}:{minutes} {day}.{month}.{year} будет включён')

    utils.apply(daemon, datetime(year, month, day))