import os
import timetable_handling.timetable_operations as timetable
from users.user_storage import * 
from logging_features.ring_logger import *
import ring_commands.ring_commands as rings
import privileges.validate as validator
import privileges.edit_admins as admins
from telebot import *

token = os.environ["BELLER_TOKEN"]

bot = TeleBot(token)

@bot.message_handler(commands=["add_admin"])
def admin_add(message):
    admins.add(bot, message)
    target = message.text.replace(' ', '')[len('/add_admin'):].replace('@', '')


@bot.message_handler(commands=["rm_admin"])
def admin_rm(message):
    admins.remove(bot, message)
    target = message.text.replace(' ', '')[len('/add_admin'):].replace('@', '')


@bot.message_handler(commands=["ring"])
def ring(message):
    if validator.check(message, UserStorage('admins').append_user('ncinsli')):
        rings.ring()
        log_sucessful_ring(message.from_user.username)

    else:
        log_unsuccessful_ring(message.from_user.username)

@bot.message_handler(commands=["add_unique"])
def add_unique(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        timetable.add_unique_day(message)

@bot.message_handler(commands=["get_timetable"])
def get_timetable(message):
    timetable.get_timetable(message)

@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, "BellBrige146 - экземпляр системы BellBrige для МАОУ СОШ №146 с углублённым изучением физики, математики, информатики г. Перми")

bot.infinity_polling()