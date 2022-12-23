import os
import sqlite3
from telebot import *
from telebot import types
from daemon.daemon import Daemon
from datetime import datetime
from dynaconf import settings
import configuration

import admins.edit 
import admins.validator
import admins.middleware

from logging_features.ring_logger import *
import timetable.middleware
import timetable.getting
import timetable.muting 


token = os.environ["BELLER_TOKEN"]
bot = TeleBot(token)

connection = configuration.connection
cursor = connection.cursor()

timetable.middleware.init()
admins.middleware.init()

date_time = datetime.now()
refreshed_timetable, refreshed_mutetable = timetable.getting.get_time(datetime(date_time.year, date_time.month, date_time.day))

daemon = Daemon(refreshed_timetable, refreshed_mutetable)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Добрый день!')

@bot.message_handler(commands=["add_admin"])
def admin_add(message):
    admins.middleware.add(bot, message)
    target = message.text.replace(' ', '')[len('/add_admin'):].replace('@', '')


@bot.message_handler(commands=["rm_admin"])
def admin_rm(message):
    admins.middleware.remove(bot, message)
    target = message.text.replace(' ', '')[len('/add_admin'):].replace('@', '')


@bot.message_handler(commands=["ring"])
def ring(message):
    if admins.validator.check(message):
        daemon.instant_ring()
        # log_sucessful_ring(message.from_user.username)

    else:
        log_unsuccessful_ring(message.from_user.username)
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["resize"])
def resize(message):
    if (admins.validator.check(message)):
        timetable.middleware.resize(bot, message, daemon)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["mute"])
def mute(message):
    if (admins.validator.check(message)):
        timetable.middleware.mute(bot, message, daemon)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["mute_all"])
def mute(message):
    if (admins.validator.check(message)):
        timetable.middleware.mute_all(bot, message, daemon)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["unmute"])
def unmute(message):
    if (admins.validator.check(message)):
        timetable.middleware.unmute(bot, message, daemon)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["shift"])
def shift(message):
    if (admins.validator.check(message)):
        timetable.middleware.shift(bot, message, daemon)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["get_timetable"])
def get_timetable(message):
    timetable.middleware.get_time(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def get_timetable_callbacks(call):
    if call.message:
        call_data = call.data.split()
        if call_data[0] == '/get_timetable':
            timetable.middleware.get_time_edited(bot, call)

@bot.message_handler(commands=["set_timetable"])
def set_timetable(message):
    if (admins.validator.check(message)):
        bot.reply_to(message,
        """Отправьте файл расписания в формате JSON по одному из шаблонов
        1. Сдвиговой формат(https://docs.github.com/......)
        2. Абсолютный формат(https://docs.github.com/.....)

❗ Обратите внимание, что при применении расписания все изменения на все дни удалятся
        """)
        bot.register_next_step_handler(message, get_new_timetable)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

def get_new_timetable(message):
    returnedMessage = timetable.middleware.set_time(bot, message, daemon)
    bot.reply_to(message, returnedMessage)

@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, "BrigeBell146 - экземпляр системы BellBrige для МАОУ СОШ №146 с углублённым изучением физики, математики, информатики г. Перми")


print(f"Starting {colored('[DAEMON]', 'blue')} and BOT")
daemon.start()
admins.edit.append(configuration.owner)

bot.infinity_polling()