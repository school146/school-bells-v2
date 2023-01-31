import json
import os
import sys
import subprocess
from telebot import *
from datetime import datetime
from daemon.daemon import Daemon
from datetime import datetime
import configuration
import replies

import admins.edit
import admins.storage
import admins.validator
import admins.middleware
import logging

from timetable.events import EventType
from logging_features.ring_logger import *
import timetable.middleware
import timetable.getting
import timetable.setting
import timetable.muting 

if not os.path.exists('logs'):
    os.system("mkdir logs")
    
log_filename = os.path.join('logs', f'{datetime.now().strftime("%a %d %b %Y %H;%M;%S")}.log')

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(log_filename), logging.StreamHandler(sys.stdout)], format='[%(asctime)s] [%(levelname)s] %(message)s')

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
        try:
            result = subprocess.check_output(message.text[5:].split())
        
            logging.warning(f'@{message.from_user.username} used unsafe command: {message.text[5:]}')
            bot.reply_to(message, result)
        except:
            logging.error(f'@{message.from_user.username} used unsafe command ({message.text[6:]}). It\'s not a Linux machine!')

    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["set_status"])
def set_status(message):
    if (admins.validator.check(message)):
        configuration.status = message.text[12:]
#       print(overAllStatus)
#       print(subprocess.check_output(message.text[5:].split()))
        logging.info(f'@{message.from_user.username} set status to: {configuration.status}')
        bot.reply_to(message, '✅ Статус поменян')

    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["state"])
def state(message):
    logging.info(f'@{message.from_user.username} requested system state')
    bot.reply_to(message, replies.get_state_reply(daemon))

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, replies.greeting)

@bot.message_handler(commands=["admins"])
def list_admin(message):
    pretty = '🌐  Администраторы\n\n' + '•  @' + str(admins.storage.get()).replace('[', '').replace(']', '').replace(' ', '').replace("'", '').replace(',', '\n•  @')
    bot.send_message(message.chat.id, pretty)

@bot.message_handler(commands=["add_admin"])
def admin_add(message):
    if (admins.validator.check(message)):
        admins.middleware.add(bot, message)
    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["rm_admin"])
def admin_rm(message):
    if (admins.validator.check(message)):
        admins.middleware.remove(bot, message)
    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["ring"])
def ring(message):
    if admins.validator.check(message):
        duration = configuration.ring_duration
        try:
            if message.text != '/ring': duration = float(message.text.split()[1])
        except: bot.reply_to(message, 'Неверный аргумент')
        daemon.instant_ring(duration)
    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["resize"])
def resize(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.resize_incorrect_format)
            logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}: invalid format')
        else:
            timetable.middleware.resize(bot, message, daemon)
            logging.info(f'@{message.from_user.username} resized timetable ({message.text})')
    else:
        bot.reply_to(message, replies.access_denied)
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')

@bot.message_handler(commands=["mute"])
def mute(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}: incorrect format')
            bot.reply_to(message, replies.mute_incorrect_format)
        else:
            logging.info(f'@{message.from_user.username} muted timetable ({message.text})')
            timetable.middleware.mute(bot, message, daemon)

    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["mute_all"])
def mute_all(message):
    if (admins.validator.check(message)):
        timetable.middleware.mute_all(bot, message, daemon)
        logging.info(f'@{message.from_user.username} muted all day ({message.text})')
    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["unmute"])
def unmute(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.unmute_incorrect_format)
            logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}: incorrect format')

        else:
            timetable.middleware.unmute(bot, message, daemon)
            logging.info(f'@{message.from_user.username} muted timetable ({message.text})')
    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["unmute_all"])
def unmute_all(message):
    if (admins.validator.check(message)):
        timetable.middleware.unmute_all(bot, message, daemon)
        logging.info(f'@{message.from_user.username} unmuted all day ({message.text})')
    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["shift"])
def shift(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.shift_incorrect_format)
            logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}: incorrect format')
        else:
            timetable.middleware.shift(bot, message, daemon)
            logging.info(f'@{message.from_user.username} shifted timetable ({message.text})')

    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["pre_ring_edit"])
def pre_ring_edit(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.pre_ring_incorrect_format)
            logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}: incorrect format')
        else:
            timetable.middleware.pre_ring_edit(bot, message)
            logging.info(f'@{message.from_user.username} edited pre-ring interval ({message.text})')
    else:
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')
        bot.reply_to(message, replies.access_denied)

@bot.message_handler(commands=["get_timetable"])
def get_timetable(message):
    timetable.middleware.get_time(bot, message)
    logging.info(f'@{message.from_user.username} requested timetable')

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
        logging.info(f'@{message.from_user.username} requested to change default timetable')
    else:
        bot.reply_to(message, replies.access_denied)
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')

def get_new_timetable(message):
    returnedMessage = timetable.middleware.set_time(bot, message, daemon)
    bot.reply_to(message, returnedMessage)
    logging.info(f'@{message.from_user.username} changed default timetable')


@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, replies.about)

@bot.message_handler(commands=["lesson_duration"])
def lesson_duration(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text or message.text.split()[1].isnumeric():
            bot.reply_to(message, replies.lesson_duration_incorrect_format)
        else:
            timetable.middleware.events_duration(bot, EventType.LESSON, message, daemon)
            bot.reply_to(message, "✅ Продолжительность уроков успешно изменена")
            logging.info(f'@{str(message.from_user.username).lower()} changed lessons duration ({message.text})')

    else:
        bot.reply_to(message, replies.access_denied)    
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')

@bot.message_handler(commands=["break_duration"])
def break_duration(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.break_duration_incorrect_format)
        else:
            timetable.middleware.events_duration(bot, EventType.BREAK, message, daemon)
            bot.reply_to(message, "✅ Продолжительность перемен успешно изменена")
            logging.info(f'@{str(message.from_user.username).lower()} changed breaks duration ({message.text})')
    else:
        bot.reply_to(message, replies.access_denied)    
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')

@bot.message_handler(commands=["add_receiver"])
def add_receiver(message):
    if (admins.validator.check(message)):
        if ' ' not in message.text:
            bot.reply_to(message, replies.add_receiver_incorrect_format)
        else:
            configuration.debug_info_receivers.add(message.text.split()[1])
            bot.reply_to(message, "✅ Пользователь добавлен")
            logging.info(f'@{str(message.from_user.username).lower()} added debug updated receiver ({message.text})')
    else:
        bot.reply_to(message, replies.access_denied)    
        logging.error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}')

print(f"Works.")
daemon.start()

try:
    with open('timetable.json', 'r') as table_file:
        table = json.loads(table_file.read())
    
        if "format" not in table:
            pass

        if table["format"] == "shift":
            returned = timetable.middleware.shift_table_handler(table)
        elif table["format"] == "absolute":
            returned = timetable.middleware.absolute_table_handler(table)
        
        new_timetable, new_muted = timetable.getting.get_time(datetime.now())
        daemon.update(new_timetable, new_muted)

except:
    logging.info('No .json file, using default configs which may not be precisient')

for owner in configuration.owners:
    admins.edit.append(owner)

bot.infinity_polling()
