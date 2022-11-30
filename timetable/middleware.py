#TODO: Каталог ошибок, кодовых номеров и соответствующих строк
INCORRECT_FORMAT_ERROR = "Ошибка при чтении файла. Неверный формат"

import sqlite3
from datetime import datetime
from telebot import TeleBot
import timetable.muting as timetable
import json
import timetable.resizing
import os
import sys
from timetable.events import EventType
from daemon.daemon import Daemon
import timetable.utils as utils
import timetable.muting
import timetable.getting
import timetable.setting
import timetable.overrides
import timetable.timetable_defaultvalues as setup

def init(connection: sqlite3.Connection):
    cursor = connection.cursor()

    table = 'bells'
    table_override = 'bell_overrides'

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table} (
        id INTEGER,
        time TEXT NOT NULL,
        OnMonday INTEGER DEFAULT 0,
        OnTuesday INTEGER DEFAULT 0,
        OnWednesday INTEGER DEFAULT 0,
        OnThursday INTEGER DEFAULT 0,
        OnFriday INTEGER DEFAULT 0,  
        OnSaturday INTEGER DEFAULT 0,
        OnSunday INTEGER DEFAULT 0,
        FromDay TEXT DEFAULT "01.09",
        TillDay TEXT  DEFAULT "31.05",
        muted INTEGER DEFAULT 0,
        PRIMARY KEY(id AUTOINCREMENT)
    ) 
    """)

    connection.commit()
    cursor.execute(f"""SELECT * FROM {table}""")
    length = len(cursor.fetchall())

    connection.commit()
    if length == 0:
        setup.do_dirty_work(connection, cursor)

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_override} (
        id INTEGER,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL,
        time TEXT NOT NULL,
        muted INTEGER DEFAULT 0,
        PRIMARY KEY(id AUTOINCREMENT)
    ) 
    """)
    connection.commit()

def get_time(bot: TeleBot, message, connection: sqlite3.Connection):

    decomposed = message.text.split()
    if len(decomposed) == 1:
        dmy = str(datetime.now().date()).split('-')
    else:
        dmy = (decomposed[1].split('.'))
        dmy.reverse()

    date = datetime(int(dmy[0]), int(dmy[1]), int(dmy[2]))

    list_db, muted = timetable.getting.get_time(connection, date)
    combined = []
    print(list_db, muted)
    for i in range(0, len(list_db) - 1):
        if i % 2 == 0:
            to_append = ('🔇' if muted[i] else '') + '<b>• ' + list_db[i] + ' — ' + list_db[i + 1] + '</b>' + ('🔇' if muted[i + 1] else '')
        else: to_append = '   ' + ('🔇' if muted[i] else '') + list_db[i] + ' — ' + list_db[i + 1] + ('🔇' if muted[i + 1] else '')

        combined.append(to_append)

    bot.parse_mode = 'HTML'
    to_out = (' ' * 4 + '\n').join(combined)

    bot.reply_to(message, f"""
    🗓 Расписание на <b>{utils.get_weekday_russian(date)}, {date.day}</b>:\n\n{to_out}
    """)

def set_time(bot: TeleBot, message, daemon: Daemon, connection: sqlite3.Connection):

    # Свойства файла для загрузки
    file_name = message.document.file_name
    file_id = message.document.file_name
    file_id_info = bot.get_file(message.document.file_id)


    content = bot.download_file(file_id_info.file_path).decode('utf-8')
    #print(content) # Текст файла
    # TODO: Загрузка json -> изменение дефолтной БД (+ скопировать старую, наверное)

    try:
        table = json.loads(content)
    except:
        return INCORRECT_FORMAT_ERROR

    if "format" not in table:
        return INCORRECT_FORMAT_ERROR

    if table["format"] == "shift":
        returned = shift_table_handler(table, connection)
    elif table["format"] == "absolute":
        returned = absolute_table_handler(table)
    else:
        return INCORRECT_FORMAT_ERROR

    new_timetable, new_muted = timetable.getting.get_time(connection, datetime.now())
    daemon.update(new_timetable, new_muted)
    
    return returned


def shift_table_handler(table, connection: sqlite3.Connection):
    bells = ['08:30', '08:50', '09:00', '09:15', '09:35', '09:45', '09:25', '09:55', '10:10', '10:30', '10:40', '10:20', '10:50', '11:05', '11:35', '11:25', '11:45', '11:55', '12:10', '12:40', '12:30', '12:50', '13:00', '13:15', '13:35', '13:45', '13:25', '13:55', '14:10', '14:30', '14:40', '14:15', '14:50', '15:00', '15:25', '15:35']
    pre_db = dict.fromkeys(bells)

    for day in ('OnMonday', 'OnTuesday', 'OnWednesday', 'OnThursday', 'OnFriday', 'OnSaturday', 'OnSunday'):
        if "enable" in table[day]:
            if not table[day]["enable"]:
                continue # в этот день звонки отключены
        firstBell = -1
        
        if "firstBell" in table[day]:
            firstBell = table[day]["firstBell"]
        
            if not utils.is_time_format(firstBell):
                return INCORRECT_FORMAT_ERROR

        if firstBell not in bells:
            firstBell = firstBell.zfill(2)
            pre_db[firstBell] = [day]
        
        else:
            if pre_db[firstBell] != None:
                pre_db[firstBell].append(day)
            
            else:
                pre_db[firstBell] = [day]

        if "shifts" in table[day]:
            for b in table[day]["shifts"]:
                if type(b) != type(0):
                    return INCORRECT_FORMAT_ERROR
            last = firstBell
            for b in table[day]["shifts"]:
                last = utils.sum_times(last, b*60)
                if last not in pre_db.keys():
                    pre_db[last] = [day]
                else:
                    if pre_db[last] != None:
                        pre_db[last].append(day)
                    else:
                        pre_db[last] = [day]
        else:
            return INCORRECT_FORMAT_ERROR

    print(pre_db.items())
    pre_db_items = sorted(list(map(lambda e: (e[0].zfill(5), e[1]), pre_db.items())))

    timetable.overrides.delete_all(connection)
    timetable.setting.set_time(connection, dict(pre_db_items))

    return "✅ Расписание успешно перезаписано"


def absolute_table_handler(table):
    bells = ['08:30', '08:50', '09:00', '09:15', '09:35', '09:45', '09:25', '09:55', '10:10', '10:30', '10:40', '10:20', '10:50', '11:05', '11:35', '11:25', '11:45', '11:55', '12:10', '12:40', '12:30', '12:50', '13:00', '13:15', '13:35', '13:45', '13:25', '13:55', '14:10', '14:30', '14:40', '14:15', '14:50', '15:00', '15:25', '15:35']
    pre_db = dict.fromkeys(bells)

    for day in ('OnMonday', 'OnTuesday', 'OnWednesday', 'OnThursday', 'OnFriday', 'OnSaturday', 'OnSunday'):
        if "enable" in table[day]:
            if table[day]["enable"] == False:
                continue # в этот день звонки отключены

        if "bells" in table[day]:
            for b in table[day]["bells"]:
                a = b.zfill(5)
                if a not in pre_db.keys():
                    pre_db[a] = [day]
                else:
                    if pre_db[a] != None:
                        pre_db[a].append(day)
                    else:
                        pre_db[a] = [day]
        else:
            return INCORRECT_FORMAT_ERROR

    timetable.overrides.delete_overrides()
    timetable.setting.set_time(dict(sorted(pre_db.items())))

    return "✅ Расписание успешно перезаписано"

def resize(bot: TeleBot, message, daemon: Daemon, connection: sqlite3.Connection):
    args = message.text.split()[1:]
    day = int(args[0].split('.')[0])
    month = int(args[0].split('.')[1])
    year = int(args[0].split('.')[2])

    event_type = args[1]
    order = int(args[2])
    delta = args[3]

    in_seconds = utils.time_literals_to_seconds(delta)

    dmy = args[0].split('.')
    date = datetime(int(dmy[2]), int(dmy[1]), int(dmy[0]))

    if event_type == 'lesson':
        timetable.resizing.resize(connection, date, EventType.LESSON, order * 2, in_seconds)

    if event_type == 'break':
        timetable.resizing.resize(connection, date, EventType.BREAK, order * 2 + 1, in_seconds)

    bot.reply_to(message, f"{'Урок' if event_type == 'lesson' else 'Перемена'} № {order} теперь {'длиннее' if in_seconds > 0 else 'короче'} на {abs(in_seconds) // 60} минут(ы)")
    
    new_timetable, new_muted = timetable.getting.get_time(connection, datetime.now())
    daemon.update(new_timetable, new_muted)

def shift(bot: TeleBot, message, daemon: Daemon, connection: sqlite3.Connection):
    args = message.text.split()[1:]

    day = int(args[0].split('.')[0])
    month = int(args[0].split('.')[1])
    year = int(args[0].split('.')[2])

    delta = args[1]
    in_seconds = 0
    postfix_index = delta.find(next(filter(str.isalpha, delta)))

    measured_value = int(delta[:postfix_index])
    postfix = delta[postfix_index:]

    if postfix == 'min': in_seconds = measured_value * 60
    if postfix == 'h': in_seconds = measured_value * 3600

    timetable.shifting.shift(connection, datetime(year, month, day), in_seconds // 60)
    bot.reply_to(message, f'Расписание на {utils.get_weekday_russian(datetime(year, month, day))}, {day} {month}, {year} сдвинуто на {in_seconds // 60} мин')

    new_timetable, new_muted = timetable.getting.get_time(connection, datetime.now())
    daemon.update(new_timetable, new_muted)


# /mute dd.mm.yyyy hh:mm
def mute(bot: TeleBot, message, daemon: Daemon, connection: sqlite3.Connection):
    args = message.text.split()[1:]

    day = int(args[0].split('.')[0])
    month = int(args[0].split('.')[1])
    year = int(args[0].split('.')[2])

    number = args[1]
    hour = int(number.split(':')[0])
    minutes = int(number.split(':')[1])

    # Сериализация
    timetable.muting.mute(connection, datetime(year, month, day, hour, minutes))
    bot.reply_to(message, f'Звонок в {hour}:{minutes} {day}.{month}.{year} не будет включён')

    new_timetable, new_muted = timetable.getting.get_time(connection, datetime.now())
    daemon.update(new_timetable, new_muted)

def unmute(bot: TeleBot, message, daemon: Daemon, connection: sqlite3.Connection):
    args = message.text.split()[1:]

    day = int(args[0].split('.')[0])
    month = int(args[0].split('.')[1])
    year = int(args[0].split('.')[2])

    number = args[1]
    hour = int(number.split(':')[0])
    minutes = int(number.split(':')[1])

    # Сериализация
    timetable.muting.unmute(connection, datetime(year, month, day, hour, minutes))
    bot.reply_to(message, f'Звонок в {hour}:{minutes} {day}.{month}.{year} будет включён')

    new_timetable, new_muted = timetable.getting.get_time(connection, datetime.now())
    daemon.update(new_timetable, new_muted)