import os
import subprocess
from telebot import *
from daemon.daemon import Daemon
from datetime import datetime
import configuration
import replies

import admins.edit 
import admins.validator
import admins.middleware

from timetable.events import EventType
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
daemon.debugger = bot

@bot.message_handler(commands=["exec"])
def exec(message):
    if (admins.validator.check(message)):
        print(subprocess.check_output(message.text[5:].split()))
        bot.reply_to(message, subprocess.check_output(message.text[5:].split()))
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["set_status"])
def set_status(message):
    if (admins.validator.check(message)):
        configuration.status = message.text[11:]
#       print(overAllStatus)
#       print(subprocess.check_output(message.text[5:].split()))
        bot.reply_to(message, '✅ Статус поменян')
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["state"])
def state(message):
    bot.reply_to(message, replies.get_state_reply(daemon))

@bot.message_handler(commands=["start"])
def start(message):
    print(message.chat.id)
    bot.send_message(message.chat.id, replies.greeting)

@bot.message_handler(commands=["add_admin"])
def admin_add(message):
    if (admins.validator.check(message)):
        admins.middleware.add(bot, message)
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["rm_admin"])
def admin_rm(message):
    if (admins.validator.check(message)):
        admins.middleware.remove(bot, message)
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["ring"])
def ring(message):
    if admins.validator.check(message):
        duration = configuration.ring_duration
        try:
            if message.text != '/ring': duration = float(message.text.split()[1])
        except: bot.reply_to(message, 'Неверный аргумент')
        daemon.instant_ring(duration)
        # log_sucessful_ring(message.from_user.username)
    else:
        log_unsuccessful_ring(message.from_user.username)
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["resize"])
def resize(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.resize_incorrect_format)
        else:
            timetable.middleware.resize(bot, message, daemon)
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["mute"])
def mute(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.mute_incorrect_format)
        else:
            timetable.middleware.mute(bot, message, daemon)
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["mute_all"])
def mute_all(message):
    if (admins.validator.check(message)):
        timetable.middleware.mute_all(bot, message, daemon)
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["unmute"])
def unmute(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.unmute_incorrect_format)
        else:
            timetable.middleware.unmute(bot, message, daemon)
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["unmute_all"])
def unmute_all(message):
    if (admins.validator.check(message)):
        timetable.middleware.unmute_all(bot, message, daemon)
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["shift"])
def shift(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.shift_incorrect_format)
        else:
            timetable.middleware.shift(bot, message, daemon)
    else:
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["pre_ring_edit"])
def pre_ring_edit(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.pre_ring_incorrect_format)
        else:
            timetable.middleware.pre_ring_edit(bot, message)
    else:
        bot.reply_to(message, replies.access_denied)

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
        bot.reply_to(message, replies.set_timetable_first)
        bot.register_next_step_handler(message, get_new_timetable)
    else:
        bot.reply_to(message, replies.access_denied)

def get_new_timetable(message):
    returnedMessage = timetable.middleware.set_time(bot, message, daemon)
    bot.reply_to(message, returnedMessage)

@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, replies.about)

@bot.message_handler(commands=["lesson_duration"])
def lesson_duration(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.lesson_duration_incorrect_format)
        else:
            timetable.middleware.events_duration(bot, EventType.LESSON, message, daemon)
            bot.reply_to(message, "✅ Продолжительность уроков успешно изменена")
    else:
        bot.reply_to(message, replies.access_denied)    

@bot.message_handler(commands=["break_duration"])
def lesson_duration(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.break_duration_incorrect_format)
        else:
            timetable.middleware.events_duration(bot, EventType.BREAK, message, daemon)
            bot.reply_to(message, "✅ Продолжительность перемен успешно изменена")
    else:
        bot.reply_to(message, replies.access_denied)    


print(f"Starting {colored('[DAEMON]', 'blue')} and BOT")
daemon.start()

for owner in configuration.owners:
    admins.edit.append(owner)

bot.infinity_polling()
